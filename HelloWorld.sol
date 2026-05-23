// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloWorld {
    string public message = "Hello World";
    string[] public messages;

    // Bulk operations constants
    uint256 public constant MAX_BULK_STORE = 50;
    uint256 public constant MAX_BULK_RETRIEVE = 100;

    // Events
    event MessageStored(uint256 indexed index, string message);
    event BulkMessagesStored(uint256 count, uint256 totalMessages);
    event BulkMessagesRetrieved(address indexed requester, uint256 count);

    // Функция для получения сообщения
    function getMessage() public view returns (string memory) {
        return message;
    }

    // Store a single message
    function storeMessage(string memory _message) public {
        messages.push(_message);
        emit MessageStored(messages.length - 1, _message);
    }

    /*//////////////////////////////////////////////////////////////
                           BULK OPERATIONS
    //////////////////////////////////////////////////////////////*/

    /// @notice Store multiple messages in a single transaction
    /// @param _messages Array of messages to store (max 50)
    function bulkStoreMessages(string[] calldata _messages) external {
        uint256 count = _messages.length;
        require(count > 0 && count <= MAX_BULK_STORE, "Invalid bulk store count");

        uint256 startIndex = messages.length;

        for (uint256 i = 0; i < count; i++) {
            messages.push(_messages[i]);
            emit MessageStored(startIndex + i, _messages[i]);
        }

        emit BulkMessagesStored(count, messages.length);
    }

    /// @notice Retrieve multiple messages by indices
    /// @param indices Array of message indices to retrieve (max 100)
    /// @return retrievedMessages Array of retrieved messages
    function bulkGetMessages(uint256[] calldata indices) external view returns (string[] memory retrievedMessages) {
        uint256 count = indices.length;
        require(count > 0 && count <= MAX_BULK_RETRIEVE, "Invalid bulk retrieve count");

        retrievedMessages = new string[](count);

        for (uint256 i = 0; i < count; i++) {
            require(indices[i] < messages.length, "Index out of bounds");
            retrievedMessages[i] = messages[indices[i]];
        }
    }

    /// @notice Get a range of messages
    /// @param startIndex Starting index (inclusive)
    /// @param count Number of messages to retrieve (max 100)
    /// @return retrievedMessages Array of messages in the range
    function getMessageRange(uint256 startIndex, uint256 count) external view returns (string[] memory retrievedMessages) {
        require(count > 0 && count <= MAX_BULK_RETRIEVE, "Invalid range count");
        require(startIndex < messages.length, "Start index out of bounds");
        require(startIndex + count <= messages.length, "Range exceeds array length");

        retrievedMessages = new string[](count);

        for (uint256 i = 0; i < count; i++) {
            retrievedMessages[i] = messages[startIndex + i];
        }
    }

    /// @notice Store messages with custom indices (allows overwriting)
    /// @param indices Array of indices to store at
    /// @param _messages Array of messages to store
    function bulkStoreAtIndices(uint256[] calldata indices, string[] calldata _messages) external {
        uint256 count = indices.length;
        require(count == _messages.length, "Indices and messages arrays must match");
        require(count > 0 && count <= MAX_BULK_STORE, "Invalid bulk store count");

        for (uint256 i = 0; i < count; i++) {
            uint256 index = indices[i];

            // Extend array if necessary
            if (index >= messages.length) {
                // Fill gaps with empty strings if needed
                for (uint256 j = messages.length; j <= index; j++) {
                    messages.push("");
                }
            }

            messages[index] = _messages[i];
            emit MessageStored(index, _messages[i]);
        }

        emit BulkMessagesStored(count, messages.length);
    }

    /// @notice Remove multiple messages by indices (set to empty string)
    /// @param indices Array of indices to clear (max 50)
    function bulkRemoveMessages(uint256[] calldata indices) external {
        uint256 count = indices.length;
        require(count > 0 && count <= MAX_BULK_STORE, "Invalid bulk remove count");

        for (uint256 i = 0; i < count; i++) {
            uint256 index = indices[i];
            require(index < messages.length, "Index out of bounds");

            messages[index] = "";
            emit MessageStored(index, "");
        }
    }

    /// @notice Get bulk operation limits
    function getBulkLimits() external pure returns (uint256 maxStore, uint256 maxRetrieve) {
        return (MAX_BULK_STORE, MAX_BULK_RETRIEVE);
    }

    /// @notice Estimate gas for bulk operations
    /// @param operationCount Number of operations
    /// @param operationType 0=store, 1=retrieve, 2=remove
    function estimateBulkGas(uint256 operationCount, uint256 operationType) external pure returns (uint256) {
        require(operationCount > 0, "Invalid count");

        uint256 baseGas = 21000;
        uint256 gasPerOperation;

        if (operationType == 0) {
            // Store operations (storage writes)
            gasPerOperation = operationCount <= MAX_BULK_STORE ? 25000 : 30000;
            require(operationCount <= MAX_BULK_STORE, "Too many store operations");
        } else if (operationType == 1) {
            // Retrieve operations (storage reads)
            gasPerOperation = 5000;
            require(operationCount <= MAX_BULK_RETRIEVE, "Too many retrieve operations");
        } else if (operationType == 2) {
            // Remove operations (storage writes)
            gasPerOperation = 20000;
            require(operationCount <= MAX_BULK_STORE, "Too many remove operations");
        } else {
            revert("Invalid operation type");
        }

        return baseGas + (gasPerOperation * operationCount);
    }

    /// @notice Get total number of messages stored
    function getMessageCount() external view returns (uint256) {
        return messages.length;
    }

    /// @notice Get messages with pagination
    /// @param page Page number (0-indexed)
    /// @param pageSize Number of messages per page (max 50)
    /// @return pageMessages Array of messages for the requested page
    function getMessagesPaginated(uint256 page, uint256 pageSize) external view returns (string[] memory pageMessages) {
        require(pageSize > 0 && pageSize <= 50, "Invalid page size");
        uint256 startIndex = page * pageSize;
        require(startIndex < messages.length, "Page out of bounds");

        uint256 endIndex = startIndex + pageSize;
        if (endIndex > messages.length) {
            endIndex = messages.length;
        }

        pageMessages = new string[](endIndex - startIndex);
        for (uint256 i = 0; i < pageMessages.length; i++) {
            pageMessages[i] = messages[startIndex + i];
        }
    }

    /// @notice Get total pages for pagination
    /// @param pageSize Number of messages per page
    /// @return totalPages Total number of pages
    function getTotalPages(uint256 pageSize) external view returns (uint256 totalPages) {
        require(pageSize > 0 && pageSize <= 50, "Invalid page size");
        totalPages = (messages.length + pageSize - 1) / pageSize;
    }

    /// @notice Search for messages containing a substring (case-sensitive)
    /// @param searchTerm The substring to search for
    /// @param maxResults Maximum number of results to return
    /// @return foundIndices Array of indices where the substring was found
    function searchMessages(string calldata searchTerm, uint256 maxResults) external view returns (uint256[] memory foundIndices) {
        require(maxResults > 0 && maxResults <= MAX_BULK_RETRIEVE, "Invalid max results");

        uint256[] memory tempResults = new uint256[](maxResults);
        uint256 resultCount = 0;

        for (uint256 i = 0; i < messages.length && resultCount < maxResults; i++) {
            if (bytes(messages[i]).length > 0) {
                // Simple substring search (case-sensitive)
                if (_containsSubstring(messages[i], searchTerm)) {
                    tempResults[resultCount] = i;
                    resultCount++;
                }
            }
        }

        // Resize array to actual result count
        foundIndices = new uint256[](resultCount);
        for (uint256 i = 0; i < resultCount; i++) {
            foundIndices[i] = tempResults[i];
        }
    }

    /// @notice Get statistics about stored messages
    /// @return totalMessages Total number of message slots
    /// @return filledMessages Number of non-empty messages
    /// @return averageLength Average message length
    function getMessageStats() external view returns (uint256 totalMessages, uint256 filledMessages, uint256 averageLength) {
        totalMessages = messages.length;
        uint256 totalLength = 0;

        for (uint256 i = 0; i < messages.length; i++) {
            if (bytes(messages[i]).length > 0) {
                filledMessages++;
                totalLength += bytes(messages[i]).length;
            }
        }

        averageLength = filledMessages > 0 ? totalLength / filledMessages : 0;
    }

    /// @notice Internal helper function to check if a string contains a substring
    function _containsSubstring(string memory haystack, string memory needle) internal pure returns (bool) {
        bytes memory h = bytes(haystack);
        bytes memory n = bytes(needle);

        if (n.length > h.length) {
            return false;
        }

        for (uint256 i = 0; i <= h.length - n.length; i++) {
            bool found = true;
            for (uint256 j = 0; j < n.length; j++) {
                if (h[i + j] != n[j]) {
                    found = false;
                    break;
                }
            }
            if (found) {
                return true;
            }
        }

        return false;
    }
}
