import json

from direct.showbase.ShowBaseGlobal import globalClock
from wecs.core import Component, System, and_filter


@Component()
class Reporting:
    repUnits = None


class ReportSystem(System):
    last_report_time = globalClock.get_frame_time()
    frequency: int = 0.5  # seconds

    entity_filters = {
        'reporters': and_filter([Reporting, ])
    }

    def enter_filter_reporters(self, entity):
        print(f"Enter REPORT {entity}   units: {entity[Reporting]}")
        print(f"current repUnits:{entity[Reporting].repUnits}")
        if entity[Reporting].repUnits is None:
            entity[Reporting].repUnits = list()
        for c in entity.get_components():
            for v in dir(c):
                if 'report_' in v:
                    # print(f"comp {c.__class__.__name__} val:{v}")
                    entity[Reporting].repUnits.append((c, v))
        print(f"entered {entity[Reporting].repUnits}")

    def update(self, entities_by_filter):
        if self.last_report_time + self.frequency > globalClock.get_frame_time():
            return
        report = []
        for reporter in entities_by_filter['reporters']:
            print(f"report for:{reporter}")
            units_reports = []
            for subUnit, k in reporter[Reporting].repUnits:
                key = f"{subUnit.__class__.__name__}.{k[7:]}"
                v = str(getattr(subUnit, k[7:], '-')).split('.')[0]
                units_reports.append({key: v})
            report.append({str(reporter): units_reports})
        print(f"done: {json.dumps(report)}")

        self.last_report_time = globalClock.get_frame_time()
        print(self.last_report_time)
