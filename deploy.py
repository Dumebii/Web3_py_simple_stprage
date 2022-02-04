from solcx import compile_standard, install_solc
import json
from web3 import Web3
_solc_version = "0.6.0"
install_solc(_solc_version)
with open("./SimpleStorage.sol", "r") as file:
    simple_stprage_file = file.read()

    # Compile our solidity
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_stprage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version=_solc_version,
    )
    print(compiled_sol)

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file) 
    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]['abi']

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    chain_id = 1337
    my_address = "0xa532276A0190698195E5079790Ce3A686f64FdD5"
    private_key = "0x3f26f1b066d46aa1102514a851059b3913d9f10587e2014d01eabfa76e904197"

    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.getTransactionCount(my_address)
    print(nonce)    
    
    transaction = SimpleStorage.constructor().buildTransaction(
        {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce}
    )
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)
