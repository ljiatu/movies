from typing import Dict

from aiodataloader import DataLoader


class AriadneDataLoader(DataLoader):
    context_key = None

    def __init__(self, *args, context: Dict, **kwargs):
        super().__init__(*args, **kwargs)

        self.context = context

    @classmethod
    def for_context(cls, context: Dict):
        key = cls.context_key
        if key is None:
            raise TypeError("Data loader %r does not define a context key" % (cls,))
        loaders = context.setdefault("loaders", {})
        if key not in loaders:
            loaders[key] = cls(context=context)
        loader = loaders[key]
        assert isinstance(loader, cls)
        return loader
