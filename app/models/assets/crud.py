
class Assets:
    @staticmethod
    def insert(asset, path, owner_id, visibility = True, limit = 0):
        # limit为0 时为无限制
        asset_len = len(asset)
        if limit != 0:
            