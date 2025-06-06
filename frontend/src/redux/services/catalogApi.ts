import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { 
  IAddItemToUnit, 
  IItem, 
  IItemCreate, 
  IKts, 
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
    addCatalogItemsToUnit: builder.mutation<IItem[], IAddItemToUnit>({
      query: (newUnitData) => ({
        url: 'catalog/units/add-items/',
        method: 'POST',
        body: newUnitData,
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
  useAddCatalogItemsToUnitMutation
} = catalogApi