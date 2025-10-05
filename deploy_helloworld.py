import json
import solcx
from web3 import Web3
import time
from params import PRIVATE_KEY  # Импортируем закрытый ключ из params.py

# 1. Настройки
rpc_url = ("https://base-mainnet.infura.io/v3/"
           "YOUR_API_KEY")  # Замените на ваш Infura API ключ
chain_id = 8453  # Chain ID для Base Mainnet
w3 = Web3(Web3.HTTPProvider(rpc_url))
account = w3.eth.account.from_key(PRIVATE_KEY)
address = account.address

# 2. Проверка подключения
if not w3.is_connected():
    print("Ошибка: не удалось подключиться к Infura RPC")
    exit()

# 3. Проверка баланса и газа
balance = w3.eth.get_balance(address) / 10**18
gas_price = w3.eth.gas_price
estimated_gas = 300000  # Лимит газа для деплоя
gas_cost_eth = (gas_price * estimated_gas) / 10**18
print(f"Баланс кошелька {address}: {balance} ETH")
print(f"Примерная стоимость деплоя: {gas_cost_eth} ETH")
if balance < gas_cost_eth:
    print("Ошибка: недостаточно средств для деплоя")
    exit()
if gas_cost_eth > 0.00001:
    print("Предупреждение: стоимость газа > 0.00001 ETH. "
          "Попробуйте позже.")
else:
    print("Стоимость газа < 0.00001 ETH — оптимально!")

# 4. Компиляция контракта
solcx.set_solc_version('0.8.20')  # Указываем версию solc
with open("HelloWorld.sol", "r") as file:
    contract_source = file.read()

compiled_sol = solcx.compile_source(contract_source, output_values=["abi", "bin"])
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]
print("ABI контракта:")
print(json.dumps(abi, indent=2))  # Диагностика

# 5. Деплой контракта
HelloWorld = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(address)
tx = HelloWorld.constructor().build_transaction({
    "from": address,
    "nonce": nonce,
    "gasPrice": gas_price,
    "gas": estimated_gas,
    "chainId": chain_id
})
signed_tx = account.sign_transaction(tx)
raw_tx_hex = signed_tx.raw_transaction.hex()
if not raw_tx_hex.startswith("0x"):
    raw_tx_hex = "0x" + raw_tx_hex
print(f"Подписанная транзакция деплоя (hex): {raw_tx_hex[:100]}...")
tx_hash = w3.eth.send_raw_transaction(raw_tx_hex)
print(f"Транзакция деплоя отправлена: https://basescan.org/tx/{tx_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Контракт развернут по адресу: {contract_address}")

# 6. Ожидание синхронизации
print("Ожидание синхронизации сети (5 секунд)...")
time.sleep(5)

# 7. Взаимодействие с контрактом
contract = w3.eth.contract(address=contract_address, abi=abi)
attempts = 3
for attempt in range(attempts):
    try:
        message = contract.functions.getMessage().call()
        print(f"Сообщение из контракта: {message}")
        break
    except Exception as e:
        print(f"Попытка {attempt + 1} не удалась: {e}")
        if attempt < attempts - 1:
            print("Повтор через 5 секунд...")
            time.sleep(5)
        else:
            print("Ошибка: не удалось вызвать функцию getMessage")
            exit()
