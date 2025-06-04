import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { ProjectNode } from '../../types/types'

const username = 'admin'
const password = 'admin'
const basicAuth = btoa(`${username}:${password}`)

export const projectsApi = createApi({
  reducerPath: 'projectsApi',
  baseQuery: fetchBaseQuery({
    baseUrl: 'https://specs.omgh.ru/api/',
    prepareHeaders: (headers) => {
      headers.set('Authorization', `Basic ${basicAuth}`)
      return headers
    },
  }),
  tagTypes: ['Project'],
  endpoints: (builder) => ({
    getProjects: builder.query<ProjectNode[], void>({
      query: () => 'projects/',
      providesTags: ['Project'],
    }),
  }),
})

export const {
  useGetProjectsQuery,
} = projectsApi
