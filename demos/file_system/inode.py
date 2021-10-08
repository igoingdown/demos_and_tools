from const import *


class INodeMeta(object):
    def __init__(self, name):
        self.__name = name
        pass


class INodeOptionalData(object):
    def __init__(self):
        pass


class Block(object):
    def __init__(self):
        self.data = [0 for _ in range(BLOCK_SIZE)]  # 4KB sequential disk


class DataBlock(Block):
    def __init__(self):
        super(self, DataBlock).__init__()
        pass


class INode(object):
    def __init__(self, name):
        self.__meta = INodeMeta(name)
        self.__optional = INodeOptionalData()
