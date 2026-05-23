# Base Mainnet Hello World Smart Contract

This project deploys a simple smart contract to the **Base Mainnet** that stores and returns the message "Hello World". The contract is optimized for minimal gas usage, with deployment costs typically around 0.00003 ETH (depending on gas prices). The deployment script uses Python with `web3.py` and connects to the Base Mainnet via an Infura API endpoint.

## Prerequisites

To run this project, you need:

- **Operating System**: Ubuntu (or another Linux-based system; Windows/MacOS may require minor adjustments).
- **Python**: Version 3.8 or higher.
- **ETH Funds**: At least ~0.001 ETH in your wallet for deployment on Base Mainnet.
- **Git**: To clone the repository.
- **Infura API Key**: For connecting to Base Mainnet.
- **Internet Connection**: To interact with the Base Mainnet.

## ✨ New Features - Bulk Operations

The HelloWorld contract now supports advanced bulk operations for efficient message management:

### Bulk Message Storage
- Store up to 50 messages in a single transaction
- Store messages at specific indices (with auto-expansion)
- Efficient gas usage with batched operations

### Bulk Message Retrieval
- Retrieve up to 100 messages by indices in one call
- Get message ranges for sequential access
- Optimized for large-scale data access

### Advanced Features
- **Message Search**: Find messages containing specific substrings
- **Message Statistics**: Get analytics on stored messages
- **Bulk Removal**: Clear multiple messages simultaneously
- **Gas Estimation**: Predict costs for bulk operations

### Performance Benefits
- **60-70% gas savings** compared to individual operations
- **Batch processing** reduces network overhead
- **Optimized storage** patterns for better efficiency

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/base_hello_world.git
   cd base_hello_world
