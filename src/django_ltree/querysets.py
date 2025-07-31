from django.db import models

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import TreeModel


class TreeQuerySet(models.QuerySet):
    def roots(self) -> models.QuerySet["TreeModel"]:
        return self.filter(path__depth=1)

    def children(self, path: str) -> models.QuerySet["TreeModel"]:
        return self.filter(path__descendants=path, path__depth=len(path) + 1)
    
    def order_by_path_numbers(self):
        """
        36982E79-1901-4E3C-9947-3F8D0120C6BB
        按照路径中的数字进行排序
        将路径转换为整数数组进行排序
        """
        return self.extra(
            select={'path_array': "cast(string_to_array(ltree2text(path), '.') AS integer[])",
                    'path_level': "nlevel(path)"},
            order_by=['path_array', 'path_level']
        )

