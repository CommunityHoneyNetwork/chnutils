import pymongo


def handle_list(arg):
    if arg:
        return arg.split(",")
    else:
        return []


def create_user(host, port, owner, ident, secret, publish, subscribe):
    publish_list = handle_list(publish)
    subscribe_list = handle_list(subscribe)
    rec = {
        "owner": owner,
        "ident": ident,
        "secret": secret,
        "publish": publish_list,
        "subscribe": subscribe_list
    }

    client = pymongo.MongoClient(host=host, port=port)
    res = client.hpfeeds.auth_key.update_one({"identifier": ident}, {"$set": rec}, upsert=True)
    client.admin.command('fsync', lock=False)
    client.close()
    return res, rec
