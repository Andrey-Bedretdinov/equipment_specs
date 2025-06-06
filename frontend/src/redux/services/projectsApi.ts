import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { IProject, IProjectCreate } from '../../types/types'

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

export const projectsApi = createApi({
  reducerPath: 'projectsApi',
  baseQuery,
  tagTypes: ['Projects'],
  endpoints: (builder) => ({
    getProjects: builder.query<IProject[], void>({
      query: () => 'projects/short',
      providesTags: ['Projects'],
    }),
    getProjectById: builder.query<IProject, string>({
      query: (id: string) => `projects/${id}`,
      providesTags: ['Projects'],
    }),

    addProject: builder.mutation<IProject, IProjectCreate>({
      query: (newProject) => ({
        url: 'projects/',
        method: 'POST',
        body: newProject,
      }),
      invalidatesTags: ['Projects'],
    }),
  }),
})

export const {
  useGetProjectsQuery,
  useGetProjectByIdQuery,
  useAddProjectMutation,
} = projectsApi