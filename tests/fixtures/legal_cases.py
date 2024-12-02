import factory
from datetime import datetime

class LegalCaseFactory(factory.Factory):
    """Factory for generating test legal cases"""
    class Meta:
        model = dict

    case_id = factory.Sequence(lambda n: f'CASE-{n}')
    title = factory.Sequence(lambda n: f'Dystopian Corp vs People {n}')
    filed_date = factory.LazyFunction(datetime.now)
    status = factory.Iterator(['pending', 'active', 'closed'])
    plaintiff = factory.Faker('company')
    defendant = factory.Faker('name')
    description = factory.Faker('paragraph')
    evidence = factory.List([factory.Faker('file_name') for _ in range(3)])

class CorporateCrimeFactory(factory.Factory):
    """Factory for generating corporate crime test cases"""
    class Meta:
        model = dict

    crime_id = factory.Sequence(lambda n: f'CORP-CRIME-{n}')
    corporation = factory.Faker('company')
    crime_type = factory.Iterator(['data_manipulation', 'ai_abuse', 'privacy_violation'])
    severity = factory.Iterator(['low', 'medium', 'high', 'critical'])
    impact = factory.Faker('paragraph')
    evidence_links = factory.List([factory.Faker('url') for _ in range(3)])
