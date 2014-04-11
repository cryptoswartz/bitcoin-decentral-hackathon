import serpent
from pyethereum import transactions, blocks, processblock, utils


key = utils.sha3('this is a great brain wallet')
addr = utils.privtoaddr(key)
genesis = blocks.Block.genesis({ addr: 10**18 })

code = serpent.compile(open('root.cll').read())
tx_make_root = transactions.Transaction.contract(0,0,10**12, 10000, code).sign(key)
code = serpent.compile(open('data.se').read())
tx_make_data = transactions.Transaction.contract(1,0,10**12, 10000, code).sign(key)
code = serpent.compile(open('tag.se').read())
tx_make_tag = transactions.Transaction.contract(2,0,10**12, 10000, code).sign(key)

root_contract = processblock.apply_tx(genesis, tx_make_root)
data_contract = processblock.apply_tx(genesis, tx_make_data)
tag_contract = processblock.apply_tx(genesis, tx_make_tag)

d_contract = data_contract.encode('hex')
t_contract = tag_contract.encode('hex')
v_contract = 0

#init root
tx_init_root = transactions.Transaction(3, 0, 10**12, 10000, root_contract, serpent.encode_datalist([d_contract, t_contract, v_contract])).sign(key)
ans = processblock.apply_tx(genesis, tx_init_root)
print ans.encode('hex')


content = "anthony is a badass"
content_hash = utils.sha3(content)

tag = "a true statement"
tag_hash = utils.sha3(tag)

vote = 1

tx_push = transactions.Transaction(4, 0, 10**12, 10000, root_contract, serpent.encode_datalist([1, content_hash])).sign(key)
ans = processblock.apply_tx(genesis, tx_push)
print ans.encode('hex')


tx_tag = transactions.Transaction(5, 0, 10**12, 10000, root_contract, serpent.encode_datalist([2, content_hash, tag_hash])).sign(key)
ans = processblock.apply_tx(genesis, tx_tag)
print ans.encode('hex')
quit()


tx_vote = transactions.Transaction(6, 0, 10**12, 10000, root_contract, serpent.encode_datalist([3, content_hash, tag_hash, vote])).sign(key)
ans = processblock.apply_tx(genesis, tx_vote)
print ans.encode('hex')

