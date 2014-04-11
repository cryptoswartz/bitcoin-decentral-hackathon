import serpent
from pyethereum import transactions, blocks, processblock, utils
from display import byte_to_string, display_user

def new_user(brain_pass):
    key = utils.sha3('this is a great brain wallet')
    addr = utils.privtoaddr(key)
    return key, addr

def make_population(N):
    users = []
    keys = [] 
    for i in xrange(N):
        key, addr = new_user('dsdmn%dvdscu7w2y%d%d'%(i, i*91, i+31))
        users.append(addr)
        keys.append(key)
    return users, keys


def genesis_block(users, coins_each=10**18):

    dd = dict(zip(users, [coins_each]*len(users)))
    gen = blocks.Block.genesis(dd)
    return gen

def init_system(genesis, key):

    code = serpent.compile(open('root.se').read())
    tx_make_root = transactions.Transaction.contract(0,0,10**12, 10000, code).sign(key)
    code = serpent.compile(open('data.se').read())
    tx_make_data = transactions.Transaction.contract(1,0,10**12, 10000, code).sign(key)
    code = serpent.compile(open('tag.se').read())
    tx_make_tag = transactions.Transaction.contract(2,0,10**12, 10000, code).sign(key)
    code = serpent.compile(open('users.se').read())
    tx_make_users = transactions.Transaction.contract(3,0,10**12, 10000, code).sign(key)

    root_contract = processblock.apply_tx(genesis, tx_make_root)
    data_contract = processblock.apply_tx(genesis, tx_make_data)
    tag_contract = processblock.apply_tx(genesis, tx_make_tag)
    users_contract = processblock.apply_tx(genesis, tx_make_users)

    d_contract = data_contract.encode('hex')
    t_contract = tag_contract.encode('hex')
    v_contract = 0
    u_contract = users_contract.encode('hex')

    #init root
    tx_init_root = transactions.Transaction(4, 0, 10**12, 10000, root_contract, serpent.encode_datalist([d_contract, t_contract, v_contract, u_contract])).sign(key)
    ans = processblock.apply_tx(genesis, tx_init_root)

    adresses = {root_contract.encode('hex'):'root', d_contract:'data', t_contract:'tags', u_contract:'users', utils.privtoaddr(key):'me'}

    return adresses

def push_content(content, title, key, genesis, root_contract, nonce):
    content_hash = utils.sha3(content)
    # push a transaction with a title.  recover title from blockchain
    tx_push = transactions.Transaction(nonce, 0, 10**12, 10000, root_contract, serpent.encode_datalist([1, content_hash, title])).sign(key)
    ans = processblock.apply_tx(genesis, tx_push)
    return content_hash

def register_name(name, key, root_contract, genesis, nonce):
    # register eth-address to a name.  recover name from blockchain.  names are not unique. but names + first 4 digits of address probably are....
    tx_register_name = transactions.Transaction(nonce, 0, 10**12, 10000, root_contract, serpent.encode_datalist([5, 'ethan'])).sign(key)
    ans = processblock.apply_tx(genesis, tx_register_name)

def tag_content(content_hash, tag, key, root_contract, genesis, nonce):
    tx_tag = transactions.Transaction(nonce, 0, 10**12, 10000, root_contract, serpent.encode_datalist([2, content_hash, tag])).sign(key)
    ans = processblock.apply_tx(genesis, tx_tag)

def vote_tag(content_hash, tag, vote, root_contract, key, genesis, nonce):
    #vote on a tag. 
    tx_vote = transactions.Transaction(nonce, 0, 10**12, 10000, root_contract, serpent.encode_datalist([3, content_hash, tag, vote])).sign(key)
    ans = processblock.apply_tx(genesis, tx_vote)



def get_content_title(content_hash, data_contract, genesis):
    a = int(content_hash.encode('hex'),16) + 1 # index of title
    jj = genesis.get_storage_data(data_contract, a)
    return hex(jj)[2:-1].decode('hex')

def get_name(user_addr, users_contract, genesis):
    jj = genesis.get_storage_data(users_contract, user_addr)
    return hex(jj)[2:-1].decode('hex')

def get_tags(content_hash, tag_contract, genesis):
    ntags = genesis.get_storage_data(tag_contract,  content_hash)
    tags = []
    for i in xrange(ntags):
        a = int(content_hash.encode('hex'),16) + 3*(i+1) # index of ith tag
        jj = genesis.get_storage_data(tag_contract, a)
        tag = hex(jj)[2:-1].decode('hex')
        tags.append(tag)
    return tags
