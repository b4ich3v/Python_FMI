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
    def __init__(self, mass: float):
        if mass <= 0:
            raise ValueError("Mass must be a positive number.")
        self.mass: float = mass
        self.used: bool = False
        self._volume: float = None  # Cached value for the volume

    def __hash__(self):
        return id(self)  # Hashing the object by its unique id

    @property
    def volume(self):
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
    dynamic_classes = {}
    all_materials = set()

    # Precompute bitmask to material names mapping for quick lookup
    _bitmask_to_materials = {
        bitmask: [name for name, bit in MATERIAL_BITS.items() if bitmask & bit]
        for bitmask in range(1, 1 << len(MATERIAL_BITS))
    }

    def __init__(self):
        self.material_bitmask = 0  # Represent current materials as a bitmask
        self.materials = set()      # Set of Material instances managed by this factory

    def __call__(self, *args, **kwargs):
        self._validate_call(args, kwargs)

        if kwargs:
            return self._create_materials(kwargs)
        else:
            return self._use_materials(args)

    def _validate_call(self, args, kwargs):
        if (args and kwargs) or (not args and not kwargs):
            raise ValueError("Invalid input.")

    def _create_materials(self, kwargs):
        materials_created = []
        for material_name, mass in kwargs.items():
            material_class = self._get_material_class(material_name)
            material = self._instantiate_material(material_class, mass)
            self._add_material(material)
            materials_created.append(material)
            self.material_bitmask |= material_class.material_bit  # Use material_class.material_bit
        return tuple(materials_created)

    def _get_material_class(self, material_name):
        material_class = self.material_classes.get(material_name)
        if material_class is None:
            raise ValueError(f"Unknown material: {material_name}")
        return material_class

    def _instantiate_material(self, material_class, mass):
        return material_class(mass)

    def _add_material(self, material):
        self.materials.add(material)  # Add to factory's materials
        Factory.all_materials.add(material)  # Add to global all_materials
        # Update the bitmask with the material's bit
        self.material_bitmask |= material.material_bit

    def _use_materials(self, materials):
        self._validate_materials(materials)
        self._mark_materials_as_used(materials)

        material_bitmask, total_mass = self._calculate_bitmask_and_mass(materials)
        new_class = self._get_or_create_dynamic_class(material_bitmask)

        new_material = self._create_new_material(new_class, total_mass)
        self.material_bitmask |= new_class.material_bit  # Set the bit for the new composite material
        return new_material

    def _validate_materials(self, materials):
        known_classes = tuple(self.material_classes.values()) + tuple(self.dynamic_classes.values())

        for material in materials:
            if not isinstance(material, known_classes):
                raise ValueError(f"Invalid material instance: {material}")
            if material.used:
                raise AssertionError(f"Material {material} is already used.")

    def _mark_materials_as_used(self, materials):
        for material in materials:
            material.used = True
            self.materials.discard(material)  # Remove from factory's materials
            self.material_bitmask &= ~material.material_bit  # Clear the bit for the used material
            Factory.all_materials.discard(material)  # Remove from global all_materials

    def _calculate_bitmask_and_mass(self, materials):
        material_bitmask = 0
        total_mass = 0
        for material in materials:
            material_bitmask |= material.material_bit  # Combine material bits using bitwise OR
            total_mass += material.mass
        return material_bitmask, total_mass

    def _get_or_create_dynamic_class(self, material_bitmask):
        # Try to find existing class by material_bitmask
        for cls in self.dynamic_classes.values():
            if cls.material_bit == material_bitmask:
                return cls
        # Generate class name
        base_materials = self._determine_base_materials(material_bitmask)
        class_name = self._generate_class_name(base_materials)
        # Check if class already exists in material_classes
        if class_name in self.material_classes:
            return self.material_classes[class_name]
        # Create new dynamic class
        return self._create_dynamic_class(material_bitmask)

    def _create_dynamic_class(self, material_bitmask):
        base_materials = self._determine_base_materials(material_bitmask)
        density = self._calculate_density(base_materials)
        class_name = self._generate_class_name(base_materials)

        attributes = {
            'density': density,
            'material_bit': material_bitmask,
        }
        new_class = type(class_name, (Material,), attributes)
        # Store the new class using the class name as the key
        self.material_classes[class_name] = new_class
        self.dynamic_classes[material_bitmask] = new_class
        return new_class

    def _determine_base_materials(self, material_bitmask):
        # Use precomputed bitmask to materials mapping for efficiency
        return self._bitmask_to_materials.get(material_bitmask, [])

    def _calculate_density(self, base_materials):
        densities = [BASE_MATERIAL_DENSITIES[name] for name in base_materials]
        return sum(densities) / len(densities)

    def _generate_class_name(self, base_materials):
        # Generate class name by sorting material names to ensure consistency
        return '_'.join(sorted(base_materials))

    def _create_new_material(self, new_class, total_mass):
        new_material = new_class(total_mass)
        self.materials.add(new_material)  # Add to factory's materials
        Factory.all_materials.add(new_material)  # Add to global all_materials
        return new_material

    def can_build(self, volume_needed):
        # Calculate total volume of current materials in this factory
        total_volume = sum(material.volume for material in self.materials)
        return total_volume >= volume_needed

    @classmethod
    def can_build_together(cls, volume_needed):
        # Calculate total volume of all materials across all factories
        total_volume = sum(material.volume for material in cls.all_materials)
        return total_volume >= volume_needed
