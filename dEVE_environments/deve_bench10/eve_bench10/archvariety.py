import math
import eve


class ArchVariety(eve.intervention.MonoPlaneStatic):
    def __init__(
        self,
        episodes_between_arch_change: int = 1,
        stop_device_at_tree_end: bool = True,
        normalize_action: bool = True,
    ) -> None:
        vessel_tree = eve.intervention.vesseltree.AorticArchRandom(
            scale_width_array = [1.0],
            scale_heigth_array = [1.0],
            episodes_between_change=episodes_between_arch_change,
            scale_diameter_array=[0.85],
            arch_types_filter=[eve.intervention.vesseltree.ArchType.I],
            seeds_vessel = [1,2,3,5,6,7,8,9,10,12,13,14,16,17,18,21,22,23,27,31,34,35,37,39,42,43,44,47,48,50,52,55,56,58,61,62,63,68,69,70,71,73,79,80,81,84,89,91,92,93,95,97,102,103,108,109,110,115,116,117,118,120,122,123,124,126,127,128,129,130,131,132,134,136,138,139,140,141,142,143,144,147,148,149,150,151,152,154,155,156,158,159,161,162,167,168,171,175,190,180]
        )
        device = eve.intervention.device.JShaped(
            name="guidewire",
            velocity_limit=(35, 3.14),
            length=450,
            tip_radius=12.1,
            tip_angle=0.4 * math.pi,
            tip_outer_diameter=0.7,
            tip_inner_diameter=0.0,
            straight_outer_diameter=0.89,
            straight_inner_diameter=0.0,
            poisson_ratio=0.49,
            young_modulus_tip=17e3,
            young_modulus_straight=80e3,
            mass_density_tip=0.000021,
            mass_density_straight=0.000021,
            visu_edges_per_mm=0.5,
            collis_edges_per_mm_tip=2,
            collis_edges_per_mm_straight=0.1,
            beams_per_mm_tip=1.4,
            beams_per_mm_straight=0.5,
            color=(0.0, 0.0, 0.0),
        )

        simulation = eve.intervention.simulation.SofaBeamAdapter(friction=0.1)

        fluoroscopy = eve.intervention.fluoroscopy.TrackingOnly(
            simulation=simulation,
            vessel_tree=vessel_tree,
            image_frequency=7.5,
            image_rot_zx=[25, 0],
            image_center=[0, 0, 0],
            field_of_view=None,
        )

        target = eve.intervention.target.CenterlineRandom(
            vessel_tree=vessel_tree,
            fluoroscopy=fluoroscopy,
            threshold=5,
            branches=["lcca", "rcca", "lsa", "rsa", "bct"],
        )

        super().__init__(
            vessel_tree,
            [device],
            simulation,
            fluoroscopy,
            target,
            stop_device_at_tree_end,
            normalize_action,
        )

    @property
    def episodes_between_arch_change(self) -> int:
        return self.vessel_tree.episodes_between_change
