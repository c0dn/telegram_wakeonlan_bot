from pyrogram import filters

whitelist_user_ids = [] # Put whitelisted user ids here


def f_func(__, _, msg):
    if msg.from_user.id in whitelist_user_ids:
        return True
    else:
        return False


whitelist_filter = filters.create(f_func)


def callback_data_filter(data, prefix=None):
    async def func(flt, _, query):
        if prefix is None:
            return flt.data == query.data
        else:
            p, d = query.data.split("_")
            if data is not None:
                return p == prefix and flt.data == d
            else:
                return p == prefix

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(func, data=data, prefix=prefix)
