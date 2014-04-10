import serpent
from pyethereum import transactions, blocks, processblock, utils

code = serpent.compile(open('root.cll').read())

key = utils.sha3('this is a great brain wallet')
addr = utils.privtoaddr(key)
genesis = blocks.Block.genesis({ addr: 10**18 })

tx_make_contract = transactions.Transaction.contract(0,0,10**12, 10000, code).sign(key)

contract = processblock.apply_tx(genesis, tx_make_contract)

content = "anthony is a badass"
content_hash = utils.sha3(content)

tag = "a true statement"
tag_hash = utils.sha3(tag)

vote = 1

tx_push = transactions.Transaction(1, 0, 10**12, 10000, contract, serpent.encode_datalist([1, content_hash])).sign(key)
ans = processblock.apply_tx(genesis, tx_push)
print ans.encode('hex')

tx_tag = transactions.Transaction(2, 0, 10**12, 10000, contract, serpent.encode_datalist([2, content_hash, tag_hash])).sign(key)
ans = processblock.apply_tx(genesis, tx_tag)
print ans.encode('hex')

tx_vote = transactions.Transaction(3, 0, 10**12, 10000, contract, serpent.encode_datalist([3, content_hash, tag_hash, vote])).sign(key)
ans = processblock.apply_tx(genesis, tx_vote)
print ans.encode('hex')
