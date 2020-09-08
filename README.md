# ПО автоматической аннотации гистологических изображений

За основу взята статья https://www.nature.com/articles/s41467-019-13647-8.

Ссылка на датасет https://wiki.cancerimagingarchive.net/display/Public/Prostate+Fused-MRI-Pathology.

Структура директорий проекта:

- images: 
  - source - исходные изображения гистологических образцов формата tif. Для удобства нумерованы числами от 1.
  - split_images - патчи исходных изображений. Также нумеруются от 1, каждый патч назван <номер_строки>_<номер_столбца>.
- results:
  -  autoencoder - веса для кодировщика, декодировщика и автокодировщика.
  -  centroids:
     - centroids_<число_центроидов>.txt - файл, который содержит центы кластеров.
     - <номер_изображения>.txt - файл, который содержит к какому кластеру относится каждый патч изображения. 
  - impact:
    - impact.txt - вероятности рака для каждого кластера изначального метода.
    - re_impact.txt -  вероятности рака для каждого кластера первой модификации (см. директорию modifications). 
    - negative_cluster.txt - число не раковых патчей для каждого кластера.
    - positive_cluster.txt - число раковых патчей для каждого кластера.
  - patch_map - содержит карту патчей для отображения (для того, чтобы сэкономит время отрисовки). Если такой карты нет, то после прорисовки она сохраниться.
    
Для понимания структуры директорий, на примере patch_map. Структура: patch_map - 20 - 7.txt. 20 - общее число кластеров, 7 - номер изображения.

Config.py - конфиги проекта (в основном задаются пути директорий).

Autoencoder.py - модель автокодировщика.

ImageWorker.py - класс для работы с изображением (разделоение на патчи + удаление патчей без ткани).

FeatureGeneration.py - класс для нахождения вероятностей рака каждого кластера (патча изображения).

CorrectImpact.py - класс для нахождения вероятности рака по 1 модификации.

ViewAutoencoderResults.py - класс, для отображения результатов обученного автокодировщика.

ViewResult.py - отображение результатов автоматической аннотации.

ДОПОЛНИТЕЛЬНО: ProbabilityForEachCLuster.py + DistanceFromClusterToCluster.py - классы для нахождения вероятности рака по 2 модификации. В отображении результатов не учитываются.

## Краткий порядок работы

1. Скачать гистологические изображения в директорию images/source. В конфиге указать CLUSTER_NUMBER - общее количество кластеров.

2. Запустить ImageWorker.py (в переменную list задать все номера изображений). Проверить директорию images_split.

3. Обучить автокодировщик (к сожалению, код самого обучения куда-то пропал, но модель описана в Autoencoder.py).

4. Веса обученного автокодировщика (кодировщика и декодировщика) положить в директорию results/autoencoder.py.

5. Запустить FeatureGeneration.py (в negative_list указать номера изображений без рака, в positive_list указать номера изображений с раком). Проверить, что в results/impact появились impact.txt, negative_cluster.txt, positive_cluster.txt.

6. Выполнить 1 модификацию (файл CorrectImpact.py) ЛИБО (в качестве проверки) скопировать файл impact.txt и назвать его re_impact.txt

7. Запустить ViewResult.py. 

P.S.Для отображения результатов был использован экран 1920 x 1080, для другого разрешения нужно будет "поиграться" с параметрами.