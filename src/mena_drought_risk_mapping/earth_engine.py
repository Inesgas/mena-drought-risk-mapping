from __future__ import annotations


def mask_mod13a3_detailed_qa(
    image,
    max_vi_quality: int = 1,
    max_vi_usefulness: int = 2,
    reject_adjacent_cloud: bool = True,
    reject_mixed_clouds: bool = True,
):
    qa = image.select("DetailedQA")
    vi_quality = qa.bitwiseAnd(0b11)
    vi_usefulness = qa.rightShift(2).bitwiseAnd(0b1111)

    mask = vi_quality.lte(max_vi_quality).And(vi_usefulness.lte(max_vi_usefulness))

    if reject_adjacent_cloud:
        adjacent_cloud = qa.rightShift(8).bitwiseAnd(1)
        mask = mask.And(adjacent_cloud.eq(0))

    if reject_mixed_clouds:
        mixed_clouds = qa.rightShift(10).bitwiseAnd(1)
        mask = mask.And(mixed_clouds.eq(0))

    return image.updateMask(mask)


def scale_mod13a3_ndvi(image, output_band: str = "ndvi"):
    return image.select("NDVI").multiply(0.0001).rename(output_band)


def scale_mod11a2_lst_celsius(image, output_band: str = "lst_c"):
    return image.select("LST_Day_1km").multiply(0.02).subtract(273.15).rename(output_band)
