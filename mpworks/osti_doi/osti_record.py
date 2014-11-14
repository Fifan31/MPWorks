import os
from pymongo import MongoClient
from monty.serialization import loadfn
from collections import OrderedDict
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

class OstiRecord(object):
    def __init__(self, mp_id, db_yaml='materials_db_dev.yaml'):
        config = loadfn(os.path.join(os.environ['DB_LOC'], db_yaml))
        client = MongoClient(config['host'], config['port'], j=False)
        client[config['db']].authenticate(config['username'], config['password'])
        materials = client[config['db']].materials
        self.mp_id = mp_id
        self.material = materials.find_one({'task_id': mp_id})
        research_org = 'Lawrence Berkeley National Laboratory (LBNL), Berkeley, CA (United States)'
        self.record_dict = OrderedDict([
            ('osti_id', ''), # empty = new submission -> new DOI
            ('dataset_type', 'GD'), # or SM?
            ('title', self._get_title()),
            ('creatorsblock', self._get_creators()),
            ('product_nos', self.mp_id),
            ('contract_nos', '??'),
            ('originating_research_org', research_org),
            ('publication_date', self._get_publication_date()),
            ('language', 'English'),
            ('country', 'US'),
            ('sponsor_org', '??'),
            ('site_url', self._get_site_url()),
            ('contact_name', 'Kristin Persson'),
            ('contact_org', 'LBNL'),
            ('contact_email', 'kapersson@lbl.gov'),
            ('contact_phone', '+1(510)486-7218'),
            ('related_resource', 'TODO'), # bibliographic info
            ('contributor_organizations', 'TODO'), # not listed in research_org
            ('subject_categories_code', '36 MATERIALS SCIENCE; 54 ENVIRONMENTAL SCIENCES'),
            ('keywords', 'TODO'),
            ('description', 'TODO')
        ])
        self.record_xml = parseString(dicttoxml(
            {'record': self.record_dict}, custom_root='records', attr_type=False
        )).toprettyxml()

    def _get_title(self):
        formula = self.material['pretty_formula']
        return 'Information on %s (%s) by MaterialsProject' % (
            formula, self.mp_id
        )

    def _get_creators(self):
        return 'TODO'

    def _get_publication_date(self):
        return self.material['created_at'].strftime('%m/%d/%Y')

    def _get_site_url(self):
        return 'https://materialsproject.org/materials/%s' % self.mp_id

