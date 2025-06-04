import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { IItem, IItemCreate, IKts, IUnit } from '../../types/types'

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
  }),
})

export const {
  useGetCatalogKtsQuery,
  useGetCatalogUnitsQuery,
  useGetCatalogItemsQuery,
  useAddCatalogItemMutation,
} = catalogApi