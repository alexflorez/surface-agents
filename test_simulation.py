import numpy as np
from surface import Surface
from water import Water
from plant import Plant
import pytest


@pytest.fixture
def create_surface():
    # filename = 'images/flat.jpg'
    filename = 'images/tinybeans.jpg'
    surface = Surface(filename)
    return surface

@pytest.fixture
def create_water(create_surface):
    surface = create_surface
    water = Water(surface)
    return water

@pytest.fixture
def create_plant(create_water):
    water = create_water
    plant = Plant(water.surface, water)
    return plant

def test_check_shape_surface(create_surface):
    surface = create_surface
    assert surface.level.shape == (10, 10)

def test_height_water(create_water):
    water = create_water
    assert np.all(water.height == 1)

def test_add_water(create_water):
    water = create_water
    water.add()
    assert np.all(water.height == 2)

def test_move_water(create_water):
    water = create_water
    qty = water.height.sum()
    water.move()
    qty_after = water.height.sum()
    assert qty == qty_after

def test_plant_in_surface(create_plant):
    plant = create_plant
    plant.seed(10)
    assert plant.seeds.sum() == 10

def test_plant_grows(create_plant):
    plant = create_plant
    plant.seed(10)
    plant.grow()
    assert plant.water.height.sum() < 100 

