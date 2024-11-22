MATERIAL_BITS = {
    'Concrete': 1 << 0,  # 1 (binary 00001)
    'Brick':    1 << 1,  # 2 (binary 00010)
    'Stone':    1 << 2,  # 4 (binary 00100)
    'Wood':     1 << 3,  # 8 (binary 01000)
    'Steel':    1 << 4,  # 16 (binary 10000)
}

BASE_MATERIAL_DENSITIES = {
    'Concrete': 2500,
    'Brick': 2000,
    'Stone': 1600,
    'Wood': 600,
    'Steel': 7700,
}

class Material:
    def __init__(self, mass):
        self.mass = mass
        self.used = False  
        self._volume = None  # Cached value for the volume

    def __hash__(self):
        return id(self)  # Hashing the object by its unique id

    @property
    def volume(self):  # Caching the Volume Calculation
        if self._volume is None:
            self._volume = self.mass / self.density
        return self._volume

class Concrete(Material):
    density = BASE_MATERIAL_DENSITIES['Concrete']
    material_bit = MATERIAL_BITS['Concrete']

class Brick(Material):
    density = BASE_MATERIAL_DENSITIES['Brick']
    material_bit = MATERIAL_BITS['Brick']

class Stone(Material):
    density = BASE_MATERIAL_DENSITIES['Stone']
    material_bit = MATERIAL_BITS['Stone']

class Wood(Material):
    density = BASE_MATERIAL_DENSITIES['Wood']
    material_bit = MATERIAL_BITS['Wood']

class Steel(Material):
    density = BASE_MATERIAL_DENSITIES['Steel']
    material_bit = MATERIAL_BITS['Steel']

class Factory:
    material_classes = {
        'Concrete': Concrete,
        'Brick': Brick,
        'Stone': Stone,
        'Wood': Wood,
        'Steel': Steel,
    }
    dynamic_classes = {}  # Stores dynamically created composite material classes
    all_materials = set()  # Set of all material instances created across all factories

    def __init__(self):
        self.materials = set()  # Set of material instances created by this factory

    def __call__(self, *args, **kwargs):
        if (args and kwargs) or (not args and not kwargs):
            raise ValueError("Call must have either positional or keyword arguments, but not both.")

        if kwargs:
            return self._create_materials(kwargs)
        else:
            return self._use_materials(args)

    def _create_materials(self, kwargs):
        materials_created = []
        for material_name, mass in kwargs.items():
            material_class = self.material_classes.get(material_name) or self.dynamic_classes.get(material_name)
            if material_class is None:
                raise ValueError(f"Unknown material: {material_name}")
            material = material_class(mass)
            self.materials.add(material)
            Factory.all_materials.add(material)
            materials_created.append(material)
        return tuple(materials_created)

    def _use_materials(self, materials):
        known_classes = tuple(self.material_classes.values()) + tuple(self.dynamic_classes.values())

        for material in materials:
            if not isinstance(material, known_classes):
                raise ValueError(f"Invalid material instance: {material}")
            if material.used:
                raise AssertionError(f"Material {material} is already used.")

        for material in materials:
            material.used = True  
            self.materials.discard(material) 
            Factory.all_materials.discard(material)   

        material_bitmask = 0
        total_mass = 0
        for material in materials:
            material_bitmask |= material.material_bit  # Combine material bits using bitwise OR
            total_mass += material.mass

        if material_bitmask in self.dynamic_classes:
            new_class = self.dynamic_classes[material_bitmask]
        else:
            # Determine base materials and their densities from the material_bitmask
            base_materials = [name for name, bit in MATERIAL_BITS.items() if material_bitmask & bit]
            densities = [BASE_MATERIAL_DENSITIES[name] for name in base_materials]
            density = sum(densities) / len(densities)
            class_name = '_'.join(sorted(base_materials))

            attributes = {
                'density': density,
                'material_bit': material_bitmask,
            }
            new_class = type(class_name, (Material,), attributes)
            self.dynamic_classes[material_bitmask] = new_class

        new_material = new_class(total_mass)
        self.materials.add(new_material)
        Factory.all_materials.add(new_material)
        return new_material

    def can_build(self, volume_needed):
        total_volume = sum(material.volume for material in self.materials)
        return total_volume >= volume_needed

    @classmethod
    def can_build_together(cls, volume_needed):
        total_volume = sum(material.volume for material in cls.all_materials)
        return total_volume >= volume_needed
