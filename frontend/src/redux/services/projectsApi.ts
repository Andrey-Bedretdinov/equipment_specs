import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { IProject } from '../../types/types'

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

export const api = createApi({
  reducerPath: 'api',
  baseQuery,
  tagTypes: ['Projects'],
  endpoints: (builder) => ({
    getProjects: builder.query<IProject[], void>({
      query: () => 'projects/',
      providesTags: ['Projects'],
    }),
  }),
})

export const {
  useGetProjectsQuery,
} = api