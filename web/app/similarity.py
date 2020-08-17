from django.conf import settings

from .face_api import FaceAPI
from .text_api import TextAPI


class Similarity:
    def calc_similarity(self, text_sim, img_sim):
        return text_sim + img_sim

    def compare_all(self, target_card, cards):
        text_api = TextAPI(target_card.bio)
        bio_sim = text_api.calc_similarlities(cards)

        face_api = FaceAPI(settings.BASE_DIR + target_card.icon.for_comparing.url)
        icon_sim = face_api.feature_detection_all(cards, settings.BASE_DIR)

        similarlities = dict(zip(bio_sim.keys(), zip(bio_sim.values(), icon_sim.values())))
        total_sim = {}
        for id, (text_sim, img_sim) in similarlities.items():
            total_sim[id] = self.calc_similarity(text_sim, img_sim)

        bio_max_id = min(bio_sim, key=bio_sim.get)
        icon_min_id = min(icon_sim, key=icon_sim.get)
        total_max_id = min(total_sim, key=total_sim.get)
        ids = {'bio': bio_max_id, 'icon': icon_min_id, 'total': total_max_id}
        sim = {'bio': bio_sim, 'icon': icon_sim, 'total': total_sim }

        return sim, ids
