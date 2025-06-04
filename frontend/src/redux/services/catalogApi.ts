import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { IKts } from '../../types/types'

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
  tagTypes: ['Kts'],
  endpoints: (builder) => ({
    getCatalogKts: builder.query<IKts[], void>({
      query: () => 'catalog/kts',
      providesTags: ['Kts'],
    }),
  }),
})

export const {
  useGetCatalogKtsQuery,
} = catalogApi