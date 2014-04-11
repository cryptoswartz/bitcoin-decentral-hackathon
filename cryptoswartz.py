import serpent
from pyethereum import transactions, blocks, processblock, utils
from display import *

def new_user(brain_pass):
    key = utils.sha3(brain_pass)
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

def write_owner(root_hash, filename):
    f = open(filename)
    d = f.readlines()
    f.close()
    d[0] = 'owner = 0x%s\n'%root_hash
    f = open(filename, 'w')
    f.writelines(d)
    f.close()

def init_system(genesis, key):
    code = serpent.compile(open('root.se').read())
    tx_make_root = transactions.Transaction.contract(0,0,10**12, 10000, code).sign(key)
    root_contract = processblock.apply_tx(genesis, tx_make_root)
    
    root_hash = root_contract.encode('hex')
    print root_hash

    f = lambda x: write_owner(root_hash, x)
    map(f, ['data.se', 'tag.se', 'users.se', 'currency.se'])

    code = serpent.compile(open('data.se').read())
    tx_make_data = transactions.Transaction.contract(1,0,10**12, 10000, code).sign(key)
    code = serpent.compile(open('tag.se').read())
    tx_make_tag = transactions.Transaction.contract(2,0,10**12, 10000, code).sign(key)
    code = serpent.compile(open('users.se').read())
    tx_make_users = transactions.Transaction.contract(3,0,10**12, 10000, code).sign(key)
    code = serpent.compile(open('currency.se').read())
    tx_make_currency = transactions.Transaction.contract(4,0,10**12, 10000, code).sign(key)

    data_contract = processblock.apply_tx(genesis, tx_make_data)
    tag_contract = processblock.apply_tx(genesis, tx_make_tag)
    users_contract = processblock.apply_tx(genesis, tx_make_users)
    currency_contract = processblock.apply_tx(genesis, tx_make_currency)

    print data_contract.encode('hex')
    print tag_contract.encode('hex')
    print users_contract.encode('hex')
    print currency_contract.encode('hex')


    d_contract = data_contract.encode('hex')
    t_contract = tag_contract.encode('hex')
    v_contract = 0
    u_contract = users_contract.encode('hex')
    c_contract = currency_contract.encode('hex')

    #init root
    tx_init_root = transactions.Transaction(5, 0, 10**12, 10000, root_contract, serpent.encode_datalist([d_contract, t_contract, v_contract, u_contract, c_contract])).sign(key)
    ans = processblock.apply_tx(genesis, tx_init_root)

    print ans
    quit()

    adresses = {root_hash:'root', d_contract:'data', t_contract:'tags', u_contract:'users', utils.privtoaddr(key):'me', c_contract:'currency'}

    return adresses

def send_money(key, to, amount, genesis, addr, root_contract):
    nonce = get_nonce(genesis, addr)
    tx_money = transactions.Transaction(nonce, 0, 10**12, 10000, root_contract, serpent.encode_datalist([to, amount])).sign(key)
    ans = processblock.apply_tx(genesis, tx_money)

def push_content(content, title, key, genesis, root_contract, addr):
    nonce = get_nonce(genesis, addr)
    content_hash = utils.sha3(content)
    # push a transaction with a title.  recover title from blockchain
    tx_push = transactions.Transaction(nonce, 0, 10**12, 10000, root_contract, serpent.encode_datalist([1, content_hash, title])).sign(key)
    ans = processblock.apply_tx(genesis, tx_push)
    print ans
    quit()
    return content_hash

def register_name(name, key, root_contract, genesis, addr):
    nonce = get_nonce(genesis, addr)
    # register eth-address to a name.  recover name from blockchain.  names are not unique. but names + first 4 digits of address probably are....
    tx_register_name = transactions.Transaction(nonce, 0, 10**2, 1, root_contract, serpent.encode_datalist([5, name])).sign(key)
    ans = processblock.apply_tx(genesis, tx_register_name)

def tag_content(content_hash, tag, key, root_contract, genesis, addr, nonce = None):
    nonce = get_nonce(genesis, addr)
       
    tx_tag = transactions.Transaction(nonce, 0, 10**2, 1, root_contract, serpent.encode_datalist([2, content_hash, tag])).sign(key)
    ans = processblock.apply_tx(genesis, tx_tag)

def vote_tag(content_hash, tag, vote, root_contract, key, genesis, addr):
    nonce = get_nonce(genesis, addr)
    #vote on a tag. 
    tx_vote = transactions.Transaction(nonce, 0, 10**2, 1, root_contract, serpent.encode_datalist([3, content_hash, tag, vote])).sign(key)
    ans = processblock.apply_tx(genesis, tx_vote)

def get_all_content(root_contract, key, genesis, addr):
    nonce = get_nonce(genesis, addr)
    tx_v = transactions.Transaction(nonce, 0, 10**12, 10000, root_contract, serpent.encode_datalist([6, 'kjsdhg'])).sign(key)
    ans = processblock.apply_tx(genesis, tx_v)
    return ans


def get_content_title(content_hash, data_contract, genesis):
    a = int(content_hash.encode('hex'),16) + 1 # index of title
    jj = genesis.get_storage_data(data_contract, a)
    return  decode_int(jj)

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
