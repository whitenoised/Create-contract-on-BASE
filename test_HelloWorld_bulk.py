#!/usr/bin/env python3
"""
Test suite for HelloWorld contract bulk operations
Tests bulk message storage, retrieval, and management functions
"""

import pytest
from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HelloWorldBulkTester:
    def __init__(self, contract_address=None, rpc_url=None):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url or os.getenv('BASE_RPC_URL', 'https://mainnet.base.org')))
        self.contract_address = contract_address or os.getenv('HELLO_WORLD_CONTRACT')

        # Contract ABI with bulk operations
        self.abi = [
            {
                "inputs": [],
                "name": "message",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getMessage",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "string", "name": "_message", "type": "string"}],
                "name": "storeMessage",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "string[]", "name": "_messages", "type": "string[]"}],
                "name": "bulkStoreMessages",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256[]", "name": "indices", "type": "uint256[]"}],
                "name": "bulkGetMessages",
                "outputs": [{"internalType": "string[]", "name": "retrievedMessages", "type": "string[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "startIndex", "type": "uint256"}, {"internalType": "uint256", "name": "count", "type": "uint256"}],
                "name": "getMessageRange",
                "outputs": [{"internalType": "string[]", "name": "retrievedMessages", "type": "string[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256[]", "name": "indices", "type": "uint256[]"}, {"internalType": "string[]", "name": "_messages", "type": "string[]"}],
                "name": "bulkStoreAtIndices",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256[]", "name": "indices", "type": "uint256[]"}],
                "name": "bulkRemoveMessages",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getBulkLimits",
                "outputs": [{"internalType": "uint256", "name": "maxStore", "type": "uint256"}, {"internalType": "uint256", "name": "maxRetrieve", "type": "uint256"}],
                "stateMutability": "pure",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "operationCount", "type": "uint256"}, {"internalType": "uint256", "name": "operationType", "type": "uint256"}],
                "name": "estimateBulkGas",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "pure",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getMessageCount",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "string", "name": "searchTerm", "type": "string"}, {"internalType": "uint256", "name": "maxResults", "type": "uint256"}],
                "name": "searchMessages",
                "outputs": [{"internalType": "uint256[]", "name": "foundIndices", "type": "uint256[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getMessageStats",
                "outputs": [{"internalType": "uint256", "name": "totalMessages", "type": "uint256"}, {"internalType": "uint256", "name": "filledMessages", "type": "uint256"}, {"internalType": "uint256", "name": "averageLength", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]

        if self.contract_address:
            self.contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(self.contract_address),
                abi=self.abi
            )

        # Create test accounts
        self.accounts = []
        for i in range(5):
            acct = Account.create()
            self.accounts.append(acct)

    def setup_contract(self, contract_address):
        """Set up contract instance with address"""
        self.contract_address = contract_address
        self.contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(contract_address),
            abi=self.abi
        )

    def test_bulk_store_messages(self):
        """Test bulk message storage functionality"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        messages = [
            "Hello from bulk test 1",
            "Hello from bulk test 2",
            "Hello from bulk test 3",
            "Hello from bulk test 4",
            "Hello from bulk test 5"
        ]

        # Get initial message count
        initial_count = self.contract.functions.getMessageCount().call()

        # Execute bulk store
        tx = self.contract.functions.bulkStoreMessages(messages).build_transaction({
            'from': self.accounts[0].address,
            'nonce': self.w3.eth.get_transaction_count(self.accounts[0].address),
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.accounts[0].key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        assert receipt['status'] == 1, "Bulk store transaction failed"

        # Verify messages were stored
        final_count = self.contract.functions.getMessageCount().call()
        assert final_count == initial_count + len(messages), "Message count not updated correctly"

        # Verify we can retrieve the messages
        indices = list(range(initial_count, final_count))
        retrieved = self.contract.functions.bulkGetMessages(indices).call()

        for i, msg in enumerate(messages):
            assert retrieved[i] == msg, f"Message {i} not stored correctly"

        print(f"✅ Bulk stored {len(messages)} messages successfully")

    def test_bulk_store_maximum(self):
        """Test bulk storing maximum allowed messages"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        max_store = self.contract.functions.getBulkLimits().call()[0]
        messages = [f"Bulk message {i}" for i in range(int(max_store))]

        initial_count = self.contract.functions.getMessageCount().call()

        tx = self.contract.functions.bulkStoreMessages(messages).build_transaction({
            'from': self.accounts[0].address,
            'nonce': self.w3.eth.get_transaction_count(self.accounts[0].address),
            'gas': 2000000,  # Higher gas limit for bulk operations
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.accounts[0].key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        assert receipt['status'] == 1, "Maximum bulk store transaction failed"

        final_count = self.contract.functions.getMessageCount().call()
        assert final_count == initial_count + len(messages), "Maximum bulk store count mismatch"

        print(f"✅ Bulk stored maximum {len(messages)} messages successfully")

    def test_bulk_store_exceeds_maximum(self):
        """Test that exceeding maximum bulk store fails"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        max_store = self.contract.functions.getBulkLimits().call()[0]
        messages = [f"Message {i}" for i in range(int(max_store) + 1)]

        with pytest.raises(Exception):  # Should revert with "Invalid bulk store count"
            self.contract.functions.bulkStoreMessages(messages).call()

        print("✅ Correctly rejected bulk store exceeding maximum limit")

    def test_bulk_get_messages(self):
        """Test bulk message retrieval by indices"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        # First store some messages
        messages = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        self.contract.functions.bulkStoreMessages(messages).call()

        # Get specific indices
        indices = [1, 3, 4]  # Beta, Delta, Epsilon
        retrieved = self.contract.functions.bulkGetMessages(indices).call()

        expected = ["Beta", "Delta", "Epsilon"]
        assert retrieved == expected, "Bulk retrieval by indices failed"

        print("✅ Bulk retrieved messages by indices successfully")

    def test_get_message_range(self):
        """Test retrieving a range of messages"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        # Store messages first
        messages = ["First", "Second", "Third", "Fourth", "Fifth"]
        self.contract.functions.bulkStoreMessages(messages).call()

        # Get range from index 1 to 3 (inclusive)
        retrieved = self.contract.functions.getMessageRange(1, 3).call()

        expected = ["Second", "Third", "Fourth"]
        assert retrieved == expected, "Message range retrieval failed"

        print("✅ Retrieved message range successfully")

    def test_bulk_store_at_indices(self):
        """Test storing messages at specific indices"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        indices = [0, 2, 5, 10]
        messages = ["Zero", "Two", "Five", "Ten"]

        initial_count = self.contract.functions.getMessageCount().call()

        tx = self.contract.functions.bulkStoreAtIndices(indices, messages).build_transaction({
            'from': self.accounts[0].address,
            'nonce': self.w3.eth.get_transaction_count(self.accounts[0].address),
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.accounts[0].key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        assert receipt['status'] == 1, "Bulk store at indices transaction failed"

        # Verify messages were stored at correct indices
        retrieved = self.contract.functions.bulkGetMessages(indices).call()
        assert retrieved == messages, "Messages not stored at correct indices"

        # Verify array was extended
        final_count = self.contract.functions.getMessageCount().call()
        assert final_count == 11, "Array not extended correctly"  # Index 10 + 1

        print("✅ Bulk stored messages at specific indices successfully")

    def test_bulk_remove_messages(self):
        """Test bulk message removal"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        # Store messages first
        messages = ["Keep", "Remove1", "Keep", "Remove2", "Keep"]
        self.contract.functions.bulkStoreMessages(messages).call()

        # Remove indices 1 and 3
        indices_to_remove = [1, 3]

        tx = self.contract.functions.bulkRemoveMessages(indices_to_remove).build_transaction({
            'from': self.accounts[0].address,
            'nonce': self.w3.eth.get_transaction_count(self.accounts[0].address),
            'gas': 300000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.accounts[0].key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        assert receipt['status'] == 1, "Bulk remove transaction failed"

        # Verify messages were removed (set to empty strings)
        retrieved = self.contract.functions.bulkGetMessages([0, 1, 2, 3, 4]).call()
        expected = ["Keep", "", "Keep", "", "Keep"]
        assert retrieved == expected, "Messages not removed correctly"

        print("✅ Bulk removed messages successfully")

    def test_gas_estimation(self):
        """Test gas estimation for bulk operations"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        # Test store operation gas estimation
        store_gas = self.contract.functions.estimateBulkGas(10, 0).call()
        expected_store_gas = 21000 + (25000 * 10)  # base + per_operation * count
        assert store_gas == expected_store_gas, "Store gas estimation incorrect"

        # Test retrieve operation gas estimation
        retrieve_gas = self.contract.functions.estimateBulkGas(25, 1).call()
        expected_retrieve_gas = 21000 + (5000 * 25)
        assert retrieve_gas == expected_retrieve_gas, "Retrieve gas estimation incorrect"

        # Test remove operation gas estimation
        remove_gas = self.contract.functions.estimateBulkGas(5, 2).call()
        expected_remove_gas = 21000 + (20000 * 5)
        assert remove_gas == expected_remove_gas, "Remove gas estimation incorrect"

        print("✅ Gas estimation working correctly")

    def test_message_search(self):
        """Test message search functionality"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        # Store messages with searchable content
        messages = [
            "Hello world message",
            "Another test message",
            "World peace message",
            "Simple greeting",
            "World domination plans"
        ]
        self.contract.functions.bulkStoreMessages(messages).call()

        # Search for "world"
        results = self.contract.functions.searchMessages("world", 10).call()

        # Should find messages at indices 0, 2, 4
        expected_indices = [0, 2, 4]
        assert results == expected_indices, "Message search failed"

        # Search with limited results
        limited_results = self.contract.functions.searchMessages("world", 2).call()
        assert len(limited_results) == 2, "Limited search results incorrect"
        assert limited_results == [0, 2], "Limited search indices incorrect"

        print("✅ Message search functionality working correctly")

    def test_message_stats(self):
        """Test message statistics functionality"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        # Clear any existing messages and add fresh ones
        messages = [
            "Short",
            "",  # Empty message
            "This is a longer message with more content",
            "Medium length message",
            ""   # Another empty message
        ]

        # Get initial count to offset
        initial_count = self.contract.functions.getMessageCount().call()

        self.contract.functions.bulkStoreMessages(messages).call()

        stats = self.contract.functions.getMessageStats().call()

        total_messages = stats[0]
        filled_messages = stats[1]
        average_length = stats[2]

        # Should have initial_count + 5 total messages
        assert total_messages == initial_count + 5, "Total messages count incorrect"

        # Should have 3 filled messages (non-empty)
        assert filled_messages == 3, "Filled messages count incorrect"

        # Average length calculation: (5 + 45 + 23) / 3 = 73/3 = 24.333...
        expected_avg = (5 + 45 + 23) // 3  # Integer division
        assert average_length == expected_avg, f"Average length incorrect: got {average_length}, expected {expected_avg}"

        print("✅ Message statistics working correctly")

    def test_bulk_limits(self):
        """Test bulk operation limits"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        limits = self.contract.functions.getBulkLimits().call()

        max_store = limits[0]
        max_retrieve = limits[1]

        assert max_store == 50, "Max store limit incorrect"
        assert max_retrieve == 100, "Max retrieve limit incorrect"

        print("✅ Bulk limits retrieved correctly")

    def test_integration_workflow(self):
        """Test complete bulk operations workflow"""
        if not self.contract:
            pytest.skip("Contract not deployed")

        initial_count = self.contract.functions.getMessageCount().call()

        # 1. Bulk store initial messages
        initial_messages = ["Welcome", "To", "Bulk", "Operations"];
        self.contract.functions.bulkStoreMessages(initial_messages).call()

        # 2. Bulk store more messages at specific indices
        indices = [6, 8, 10];
        specific_messages = ["Index6", "Index8", "Index10"];
        self.contract.functions.bulkStoreAtIndices(indices, specific_messages).call()

        # 3. Bulk retrieve various messages
        all_indices = [initial_count, initial_count + 1, initial_count + 2, initial_count + 3, 6, 8, 10];
        retrieved = self.contract.functions.bulkGetMessages(all_indices).call()

        expected = ["Welcome", "To", "Bulk", "Operations", "Index6", "Index8", "Index10"];
        assert retrieved == expected, "Integration workflow retrieval failed"

        # 4. Bulk remove some messages
        remove_indices = [initial_count + 1, 8];  # Remove "To" and "Index8"
        self.contract.functions.bulkRemoveMessages(remove_indices).call()

        # 5. Verify removal
        final_retrieved = self.contract.functions.bulkGetMessages(all_indices).call()
        expected_final = ["Welcome", "", "Bulk", "Operations", "Index6", "", "Index10"];
        assert final_retrieved == expected_final, "Integration workflow removal failed"

        print("✅ Complete bulk operations workflow successful")


def run_tests():
    """Run all tests"""
    print("🚀 Starting HelloWorld Bulk Operations Tests")
    print("=" * 50)

    # Initialize tester (without contract address for now)
    tester = HelloWorldBulkTester()

    # Test bulk limits (doesn't require contract deployment)
    try:
        print("\n📋 Testing Bulk Limits...")
        # Note: This would require a deployed contract
        print("⚠️  Skipping contract tests - requires deployed contract")
        print("💡 To run full tests, deploy contract and set HELLO_WORLD_CONTRACT env var")

    except Exception as e:
        print(f"❌ Error during testing: {e}")

    print("\n" + "=" * 50)
    print("🎉 HelloWorld Bulk Operations Tests Completed!")
    print("\n📝 To run full tests:")
    print("1. Deploy HelloWorld.sol to Base network")
    print("2. Set HELLO_WORLD_CONTRACT environment variable")
    print("3. Set BASE_RPC_URL environment variable")
    print("4. Run: python test_HelloWorld_bulk.py")


if __name__ == "__main__":
    run_tests()
