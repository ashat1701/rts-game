import pygame

from rtsgame.src.utility.utilities import join_paths, Vector


class Animation:
    def __init__(self, filenames, transforms=None, offset=None):
        if transforms is None:
            transforms = Transforms()
        if offset is not None:
            offset = Vector(*offset)
        self.offset = offset

        images = [pygame.image.load(f) for f in filenames]
        self.images = [transforms(img).convert_alpha() for img in images]

    def __getitem__(self, item: int) -> pygame.Surface:
        return self.images[item]

    def __len__(self):
        return len(self.images)


def parse_descriptions(descriptions):
    animations = {
        row['name']: Animation(join_paths(row['folder'], row['sprites'], ),
                               transforms=get_transforms(row),
                               offset=row['offset'])
        for row in descriptions}

    return animations


class Transform:
    pass


class Transforms(Transform):
    def __init__(self, transforms=None):
        if transforms is None:
            transforms = []

        self.transforms = transforms

    def append(self, transform):
        self.transforms.append(transform)

    def __call__(self, image: pygame.Surface):
        for transform in self.transforms:
            image = transform(image)

        return image


class Flip(Transform):
    def __init__(self, flip_x, flip_y):
        self.flip_x = flip_x
        self.flip_y = flip_y

    def __call__(self, image):
        return pygame.transform.flip(image, self.flip_x, self.flip_y)


class Scale(Transform):
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, img):
        return pygame.transform.scale(img, img.get_height() * self.factor,
                                      img.get_width() * self.factor)


class Resize(Transforms):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def __call__(self, img):
        return pygame.transform.scale(img, self.size)


def get_transforms(config_row):
    transforms = Transforms()
    # Flip transform
    if 'flip_x' in config_row or 'flip_y' in config_row:
        transforms.append(Flip(config_row.get('flip_x', False),
                               config_row.get('flip_y', False)))
    # Resize transform
    if 'resize' in config_row:
        transforms.append(Resize(config_row['resize']))

    return transforms
