import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { ItemNode } from '../../types/types'

const username = 'admin'
const password = 'admin'
const basicAuth = btoa(`${username}:${password}`)

export const itemsApi = createApi({
  reducerPath: 'itemsApi',
  baseQuery: fetchBaseQuery({
    baseUrl: 'https://specs.omgh.ru/api/',
    prepareHeaders: (headers) => {
      headers.set('Authorization', `Basic ${basicAuth}`)
      return headers
    },
  }),
  tagTypes: ['Item'],
  endpoints: (builder) => ({
    getCatalogItems: builder.query<ItemNode[], void>({
      query: () => 'catalog/items/',
      providesTags: ['Item'],
    }),
  }),
})

export const {
  useGetCatalogItemsQuery,
} = itemsApi
