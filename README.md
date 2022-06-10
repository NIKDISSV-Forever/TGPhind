#### Documentation in Russian

> pip install [TGPhind](https://pypi.org/project/TGPhind/)


**TGPhind** - Инструмента для поиска стотей на сайте telegra.ph

# CLI

> python -m TGPhind -h

# Usage

```python
from TGPhind import TGPhind, Proxy

se = TGPhind(MAX_TH: int = None,
                           proxy: Proxy = None,
                                          brackets = '<>')
print(*se.map_hosts(se.search('article<s>-<a-d>')), sep='\n')
# query = (article-a, article-b, article-c, article-d, articles-a, articles-b, articles-c, articles-d)
```
