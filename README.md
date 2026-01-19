# Base Mainnet Hello World Smart Contract

This project deploys a simple smart contract to the **Base Mainnet** that stores and returns the message "Hello World". The contract is optimized for minimal gas usage, with deployment costs typically around 0.00003 ETH (depending on gas prices). The deployment script uses Python with `web3.py` and connects to the Base Mainnet via an Infura API endpoint.

## Features

- 🚀 Deploy a minimal "Hello World" smart contract to Base Mainnet
- ⛽ Gas-optimized deployment (~0.00003 ETH)
- 🐍 Python-based deployment using `web3.py`
- 🔗 Infura RPC integration for reliable connectivity

## Prerequisites

To run this project, you need:

- **Operating System**: Ubuntu (or another Linux-based system; Windows/MacOS may require minor adjustments)
- **Python**: Version 3.8 or higher
- **ETH Funds**: At least ~0.001 ETH in your wallet for deployment on Base Mainnet
- **Git**: To clone the repository
- **Infura API Key**: For connecting to Base Mainnet (get one at [infura.io](https://infura.io))
- **Internet Connection**: To interact with the Base Mainnet

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/whitenoised/Create-contract-on-BASE.git
   cd Create-contract-on-BASE
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install web3 py-solc-x
   ```

3. **Install Solidity Compiler**:
   ```bash
   python -c "import solcx; solcx.install_solc('0.8.20')"
   ```

## Configuration

1. **Set Your Private Key**:
   
   Edit `params.py` and replace `YOUR_WALLET_PRIVATE_KEY` with your actual wallet private key:
   ```python
   PRIVATE_KEY = "your_private_key_here"
   ```
   
   ⚠️ **Security Warning**: Never commit your private key to version control. Consider using environment variables instead.

2. **Set Your Infura API Key**:
   
   Edit `deploy_helloworld.py` and replace `YOUR_API_KEY` with your Infura API key:
   ```python
   rpc_url = "https://base-mainnet.infura.io/v3/your_api_key_here"
   ```

## Usage

Run the deployment script:

```bash
python deploy_helloworld.py
```

The script will:
1. Connect to Base Mainnet via Infura
2. Check your wallet balance
3. Estimate deployment gas costs
4. Compile the HelloWorld.sol contract
5. Deploy the contract to Base Mainnet
6. Verify the deployment by calling `getMessage()`

### Expected Output

```
Баланс кошелька 0x...: X.XXX ETH
Примерная стоимость деплоя: 0.00003 ETH
Стоимость газа < 0.00001 ETH — оптимально!
ABI контракта:
[...]
Транзакция деплоя отправлена: https://basescan.org/tx/0x...
Контракт развернут по адресу: 0x...
Сообщение из контракта: Hello World
```

## Smart Contract

The `HelloWorld.sol` contract is minimal and gas-efficient:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloWorld {
    string public message = "Hello World";

    function getMessage() public view returns (string memory) {
        return message;
    }
}
```

## Project Structure

```
Create-contract-on-BASE/
├── HelloWorld.sol        # Solidity smart contract
├── deploy_helloworld.py  # Python deployment script
├── params.py             # Configuration (private key)
├── README.md             # This file
└── .github/
    └── workflows/        # GitHub Actions
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ошибка: не удалось подключиться к Infura RPC" | Check your Infura API key and internet connection |
| "Ошибка: недостаточно средств для деплоя" | Add more ETH to your wallet (need ~0.001 ETH) |
| "Попытка X не удалась" | Network congestion - the script will retry automatically |

## Network Information

| Parameter | Value |
|-----------|-------|
| Network | Base Mainnet |
| Chain ID | 8453 |
| Currency | ETH |
| Block Explorer | [basescan.org](https://basescan.org) |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source. See the repository for license details.

## Disclaimer

⚠️ **Use at your own risk**. This project interacts with blockchain networks and requires real cryptocurrency. Always:
- Keep your private keys secure
- Test on testnet first if possible
- Verify gas costs before deployment
- Never share your private key
