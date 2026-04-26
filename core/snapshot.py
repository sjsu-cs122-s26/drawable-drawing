class Snapshot():
    def __init__(self, size, layer_blocks: list, currentLayerIndex : int, lifetimelayers: int):
        self.blocks = [{"name":layer_block.layerName, "image":layer_block.layer.image.copy(), "opacity":layer_block.layer.opacity} for layer_block in layer_blocks]
        self.canvasSize = size
        self.currentLayerIndex = currentLayerIndex
        self.lifetime_layers = lifetimelayers
