// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloWorld {
    string public message = "Hello World";

    // Функция для получения сообщения
    function getMessage() public view returns (string memory) {
        return message;
    }
}
