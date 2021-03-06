from direct.showbase.ShowBaseGlobal import globalClock
from wecs.core import Component, System, and_filter


@Component()
class Platform:
    """
    Has mass and temperature.
    """
    mass: int  # mass - Kg
    temp: int = 20  # degrees celsius
    report_temp = None


class HeatSystem(System):
    entity_filters = {
        'platform': and_filter([Platform, ]),
    }

    HEAT_EXCHANGE_FACTOR = 0.2
    ENV_TEMP = 20  # deg celsius
    ENV_HEAT_LOSS = 1000  # kcal

    def enter_filter_platform(self, entity):
        total_mass = 0
        for c in entity.get_components():
            if 'mass' in dir(c):
                total_mass += c.mass
        entity[Platform].mass = total_mass

    def update(self, entities_by_filter):
        for entity in entities_by_filter['platform']:
            if entity[Platform].temp > self.ENV_TEMP:
                entity[Platform].temp -= (self.ENV_HEAT_LOSS / entity[
                    Platform].mass) * self.HEAT_EXCHANGE_FACTOR * globalClock.dt

    def exchange_heat(self, component):
        """
        Exchange heat between component and it's platform, by calculating total kcals
        in between them, and moving the energy between them.
        """
        # Calculate total kcals in both component and platform
        comp_kcals = component.mass * component.temp
        plat_kcals = component.platform.mass * component.platform.temp
        total_kcals = comp_kcals + plat_kcals
        total_mass = component.mass + component.platform.mass
        # target is the "final" temp for component after infinity time
        target_comp_kcals = total_kcals / total_mass * component.mass
        exchange_rate_factor = self.HEAT_EXCHANGE_FACTOR * globalClock.dt
        # amount of heat to move from comp to platform
        delta_kcals = (target_comp_kcals - comp_kcals) * exchange_rate_factor
        # update component and platform temps
        component.temp = component.temp + delta_kcals / component.mass
        component.platform.temp = component.platform.temp - delta_kcals / component.platform.mass
