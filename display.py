import serpent
from pyethereum import transactions, blocks, processblock, utils

def byte_to_string(jj):
    if type(jj) == int:
       return jj
    if type(jj) == long:
        if len(str(jj)) %2 != 0:
            return int(jj)
    return hex(jj)[2:-1].decode('hex')

def display_user(genesis, user_contract, user_addr):
    print ''
    ad = int(user_addr,16)
    name = genesis.get_storage_data(user_contract, ad)
    ncontent = genesis.get_storage_data(user_contract, ad+1)
    ntags = genesis.get_storage_data(user_contract, ad+2)
    nvotes = genesis.get_storage_data(user_contract, ad+3)
    prep = genesis.get_storage_data(user_contract, ad+5)
    trep = genesis.get_storage_data(user_contract, ad+6)
    vrep = genesis.get_storage_data(user_contract, ad+7)

    deets = [name, ncontent, ntags, nvotes, prep, trep, vrep]
    deets = map(byte_to_string, deets)
    
    keys = ['name', 'ncontent', 'ntags', 'nvotes', 'pubrep', 'tagrep', 'voterep']
    print zip(keys, deets)

def get_nonce(genesis, addr):
    di = genesis.to_dict()
    state = di['state']
    for k in state.keys():
        if k == addr:
            return int((state[k])[0])
    return 0

def display_block_chain(genesis, addrs):
    di = genesis.to_dict()
    state = di['state']
    print 'keys!'
    print state.keys()
    print 'loop!'
    print addrs    
    for k in state.keys():
        if addrs.has_key(k.decode(encoding='UTF-8')):
            print addrs[k], k 
            print addrs
        else:
            print k
        for s in state[k]:
            if type(s) == long:
                print s
            elif type(s) == dict:
                for j in s.keys():
                    if type(s[j]) == long: print s[j]
                    else:
                        print s[j].encode(encoding='UTF-8')
                
            else:
                print s.encode('hex')
        print ''
    quit()
