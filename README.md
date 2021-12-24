#### Documentation in Russian

> pip install [TGPhind](https://pypi.org/project/TGPhind/)


**TGPhind** - Инструмента для поиска стотей на сайте telegra.ph

_И его зеркалах._

## Основной класс ```TGPhind```

```python
MIRRORS = ['te.legra.ph', 'graph.org', 'telegra.ph']


@dataclass
class Proxy:
    host: str = ''
    protocol: str = 'https'

    def __bool__(self): ...


class TGPhind:
    def __init__(self, article_name: str,
                 MAX_TH: Any = cpu_count(),
                 proxy: Proxy = Proxy(),
                 BRACKETS='<>'):
        ...

    @property
    def result(self) -> Union[tuple[str], tuple]: ...

    def only_paths(self) -> tuple[str]:
        return self.result

    def hosts_map(self, mirrors=None) -> tuple[tuple[str]]:
        """
        Вернёт кортеж кортежей строк
        Со всеми возможными зеркалами этой статьи (mirrors или MIRRORS)"""
        ...

    def test_mirrors(self):
        """Протестировать рабочии-ли зеркала и удалить нерабочии"""
        ...
```
