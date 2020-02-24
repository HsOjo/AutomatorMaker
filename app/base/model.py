class BaseModel:
    _sub_model = {}  # key: container_type, type
    _ignore_attrs = []

    @property
    def data(self):
        data = {}
        for k in dir(self):
            if k[0] != '_' and k != 'data':
                v = getattr(self, k)
                if isinstance(v, BaseModel):
                    v = v.data
                if not callable(v):
                    data[k] = v
        return data

    def load_data(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._ignore_attrs:
                continue
            i = getattr(self, k)
            if isinstance(i, BaseModel):
                if k not in i._sub_model:
                    i.load_data(**v)
                    v = i
                else:
                    c_type, v_type = i._sub_model[k]
                    if c_type == list:
                        items = []
                        for i in v:
                            item = v_type()  # type: BaseModel
                            item.load_data(**i)
                            items.append(item)
                        v = items
                    elif c_type == dict:
                        items = {}
                        for k_, v_ in v.items():
                            item = v_type()  # type: BaseModel
                            item.load_data(**v_)
                            items[k_] = item
                        v = items
                    else:
                        raise Exception('Unsupport Type.')
            setattr(self, k, v)
