# -*- coding: utf-8 -*-
"""
Defines functions for converting AiiDA Data to and from bands-inspect format.
"""

import typing as ty
from functools import singledispatch

from aiida import orm

from bands_inspect.kpoints import KpointsBase, KpointsExplicit, KpointsMesh
from bands_inspect.eigenvals import EigenvalsData

__all__ = ('from_bands_inspect', 'to_bands_inspect')


@singledispatch
def from_bands_inspect(
    data: ty.Union[KpointsBase, EigenvalsData]
) -> ty.Union[orm.KpointsData, orm.BandsData]:
    """Convert bands-inspect data instances into AiiDA data nodes."""
    raise NotImplementedError(
        f'Cannot convert data type {type(data)} to AiiDA data.'
    )


@from_bands_inspect.register(KpointsMesh)
def _from_bands_inspect_kpoints_mesh(data: KpointsMesh) -> orm.KpointsData:
    kpoints = orm.KpointsData()
    kpoints.set_kpoints_mesh(mesh=data.mesh, offset=data.offset)
    return kpoints


@from_bands_inspect.register(KpointsExplicit)
def _from_bands_inspect_kpoints_explicit(
    data: KpointsExplicit
) -> orm.KpointsData:
    kpoints = orm.KpointsData()
    kpoints.set_kpoints(data.kpoints)
    return kpoints


@from_bands_inspect.register(EigenvalsData)
def _from_bands_inspect_eigenvals_data(data: EigenvalsData) -> orm.BandsData:
    bands = orm.BandsData()
    kpoints = from_bands_inspect(data.kpoints)
    if 'mesh' in kpoints.attributes:
        bands.set_kpoints(kpoints.get_kpoints_mesh(print_list=True))
    else:
        bands.set_kpointsdata(kpoints)
    bands.set_bands(data.eigenvals)
    return bands


@singledispatch
def to_bands_inspect(
    data: ty.Union[orm.KpointsData, orm.BandsData]
) -> ty.Union[KpointsBase, EigenvalsData]:
    """Convert AiiDA data nodes into bands-inspect data instances."""
    raise NotImplementedError(
        f'Cannot convert data type {type(data)} to bands-inspect object.'
    )


@to_bands_inspect.register(orm.KpointsData)
def _kpointsdata_to_bands_inspect(data: orm.KpointsData) -> KpointsBase:
    attributes = data.attributes
    if 'mesh' in attributes:
        return KpointsMesh(
            mesh=attributes['mesh'], offset=attributes['offset']
        )
    if 'array|kpoints' in attributes:
        return KpointsExplicit(kpoints=data.get_kpoints())
    raise NotImplementedError(
        f"Unrecognized KpointsData form, has attributes '{attributes}'"
    )


@to_bands_inspect.register(orm.BandsData)
def _bandsdata_to_bands_inspect(data: orm.BandsData) -> EigenvalsData:
    bands_arr = data.get_bands()
    if len(bands_arr.shape) == 3:
        assert bands_arr.shape[0] == 1
        bands_arr = bands_arr[0, :, :]
    return EigenvalsData(
        kpoints=_kpointsdata_to_bands_inspect(data), eigenvals=bands_arr
    )
