import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type {
  IAddItemToUnit,
  IAddUnitsAndItemsToKts,
  IItem,
  IItemCreate,
  IKts,
  IKtsCreate,
  IUnit,
  IUnitCreate
} from '../../types/types'

const username = 'admin'
const password = 'admin'
const basicAuth = btoa(`${username}:${password}`)

const baseQuery = fetchBaseQuery({
  baseUrl: 'https://specs.omgh.ru/api/',
  prepareHeaders: (headers) => {
    headers.set('Authorization', `Basic ${basicAuth}`)
    return headers
  },
})

export const catalogApi = createApi({
  reducerPath: 'catalogApi',
  baseQuery,
  tagTypes: ['Kts', 'Units', 'Items'],
  endpoints: (builder) => ({
    getCatalogKts: builder.query<IKts[], void>({
      query: () => 'catalog/kts',
      providesTags: ['Kts'],
    }),
    getCatalogUnits: builder.query<IUnit[], void>({
      query: () => 'catalog/units',
      providesTags: ['Units'],
    }),
    getCatalogItems: builder.query<IItem[], void>({
      query: () => 'catalog/items',
      providesTags: ['Items'],
    }),


    addCatalogItem: builder.mutation<IItem, IItemCreate>({
      query: (newItem) => ({
        url: 'catalog/items/',
        method: 'POST',
        body: newItem,
      }),
      invalidatesTags: ['Items'],
    }),
    addCatalogUnit: builder.mutation<IUnit, IUnitCreate>({
      query: (newUnit) => ({
        url: 'catalog/units/',
        method: 'POST',
        body: newUnit,
      }),
      invalidatesTags: ['Units'],
    }),
    addCatalogItemsToUnit: builder.mutation<IUnit, IAddItemToUnit>({
      query: (newUnitData) => ({
        url: 'catalog/units/add-items/',
        method: 'POST',
        body: newUnitData,
      }),
      invalidatesTags: ['Units'],
    }),
    addCatalogKts: builder.mutation<IKts, IKtsCreate>({
      query: (newKts) => ({
        url: 'catalog/kts/',
        method: 'POST',
        body: newKts,
      }),
      invalidatesTags: ['Kts'],
    }),
    addUnitsAndItemsToKts: builder.mutation<IKts, IAddUnitsAndItemsToKts>({
      query: (newKtsData) => ({
        url: 'catalog/kts/add-elements/',
        method: 'POST',
        body: newKtsData,
      }),
      invalidatesTags: ['Kts'],
    }),


    deleteItem: builder.mutation<void, number>({
      query: (id: number) => ({
        url: `catalog/items/${id}/`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Items'],
    }),
    deleteKts: builder.mutation<void, number>({
      query: (id: number) => ({
        url: `catalog/kts/${id}/`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Kts'],
    }),
    deleteUnit: builder.mutation<void, number>({
      query: (id: number) => ({
        url: `catalog/units/${id}/`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Units'],
    }),
  }),
})

export const {
  useGetCatalogKtsQuery,
  useGetCatalogUnitsQuery,
  useGetCatalogItemsQuery,
  useAddCatalogItemMutation,
  useAddCatalogUnitMutation,
  useAddCatalogItemsToUnitMutation,
  useAddCatalogKtsMutation,
  useAddUnitsAndItemsToKtsMutation,
  useDeleteItemMutation,
  useDeleteKtsMutation,
  useDeleteUnitMutation,
} = catalogApi