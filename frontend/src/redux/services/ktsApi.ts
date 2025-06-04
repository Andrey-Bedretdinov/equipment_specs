import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { IProjectKtsLink } from '../../types/types'

const username = 'admin'
const password = 'admin'
const basicAuth = btoa(`${username}:${password}`)

export const ktsApi = createApi({
  reducerPath: 'ktsApi',
  baseQuery: fetchBaseQuery({
    baseUrl: 'https://specs.omgh.ru/api/',
    prepareHeaders: (headers) => {
      headers.set('Authorization', `Basic ${basicAuth}`)
      return headers
    },
  }),
  tagTypes: ['Kts'],
  endpoints: (builder) => ({
    getProjectKtsLinks: builder.query<IProjectKtsLink[], number>({
      query: (project_id: number) => `projects/${project_id}/kts/`,
      providesTags: ['Kts'],
    }),
  }),
})

export const {
  useGetProjectKtsLinksQuery,
} = ktsApi
