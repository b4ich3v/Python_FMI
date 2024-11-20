class Material:
    def __init__(self, mass):
        self.mass = mass
        self.used = False  
        self._volume = None  # Cached value for the volume

    def __hash__(self):
        return id(self)  # Hashing the object by its unique id

    def __eq__(self, other):
        return self is other  

    @property
    def volume(self):  # Caching the Volume Calculation
        if self._volume is None:
            self._volume = round(self.mass / self.density, 2)
        return self._volume


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

class Concrete(Material):
    density = 2500
    base_materials = {'Concrete'}
    material_bit = MATERIAL_BITS['Concrete']


class Brick(Material):
    density = 2000
    base_materials = {'Brick'}
    material_bit = MATERIAL_BITS['Brick']


class Stone(Material):
    density = 1600
    base_materials = {'Stone'}
    material_bit = MATERIAL_BITS['Stone']


class Wood(Material):
    density = 600
    base_materials = {'Wood'}
    material_bit = MATERIAL_BITS['Wood']


class Steel(Material):
    density = 7700
    base_materials = {'Steel'}
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
            raise ValueError("Error")

        # Local references for faster access
        material_classes = Factory.material_classes
        dynamic_classes = Factory.dynamic_classes
        all_materials = Factory.all_materials

        known_classes = tuple(material_classes.values()) + tuple(dynamic_classes.values())

        if kwargs:
            materials_created = []
            for material_name, mass in kwargs.items():
                material_class = material_classes.get(material_name) or dynamic_classes.get(material_name)
                if material_class is None:
                    raise ValueError(f"Unknown material: {material_name}")
                material = material_class(mass)
                self.materials.add(material)
                all_materials.add(material)
                materials_created.append(material)
            return tuple(materials_created)
        else:
            for material in args:
                if not isinstance(material, known_classes):
                    raise ValueError("Error")
                if material.used:
                    raise AssertionError("Error")
            for material in args:
                material.used = True  
                self.materials.discard(material) 
                all_materials.discard(material)   

            material_bitmask = 0
            total_mass = 0
            for material in args:
                material_bitmask |= material.material_bit  # Combine material bits using bitwise OR
                total_mass += material.mass

            if material_bitmask in dynamic_classes:
                new_class = dynamic_classes[material_bitmask]
            else:
                # Determine base materials and their densities from the material_bitmask
                base_materials = []
                densities = []
                for material_name, bit in MATERIAL_BITS.items():
                    if material_bitmask & bit:  # Check if material is included using bitwise AND
                        base_materials.append(material_name)
                        densities.append(BASE_MATERIAL_DENSITIES[material_name])
                density = sum(densities) / len(densities)
                class_name = '_'.join(sorted(base_materials))

                attributes = {
                    'density': density,
                    'base_materials': set(base_materials),
                    'material_bit': material_bitmask,
                }
                new_class = type(class_name, (Material,), attributes)
                dynamic_classes[material_bitmask] = new_class

            new_material = new_class(total_mass)
            self.materials.add(new_material)
            all_materials.add(new_material)
            return new_material

    def can_build(self, volume_needed):
        total_volume = 0
        for material in self.materials:
            total_volume += material.volume
            if total_volume >= volume_needed:
                return True  # Early exit if required volume is met
        return False

    @classmethod
    def can_build_together(cls, volume_needed):
        total_volume = 0
        for material in cls.all_materials:
            total_volume += material.volume
            if total_volume >= volume_needed:
                return True  # Early exit if required volume is met
        return False
