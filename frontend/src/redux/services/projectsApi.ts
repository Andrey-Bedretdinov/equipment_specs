import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { IAddElementsToProjects, IDeleteElementsFromProjects, IProject, IProjectCreate } from '../../types/types'

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
    addElementsToProject: builder.mutation<IProject, {id:number }&IAddElementsToProjects>({
      query: ({items, units, kts, id}) => ({
        url: `projects/${id}/add_elements/`,
        method: 'POST',
        body: {items, units, kts},
      }),
      invalidatesTags: ['Projects'],
    }),


    deleteProject: builder.mutation<void, number>({
      query: (id: number) => ({
        url: `projects/${id}/`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Projects'],
    }),
    deleteElementsFromProject: builder.mutation<IProject, {project_id:string}&IDeleteElementsFromProjects>({
      query: ({project_id, items, units, kts}) => ({
        url: `projects/${project_id}/`,
        method: 'PUT',
        body: {items, units, kts}
      }),
      invalidatesTags: ['Projects'],
    }),
  }),
})

export const {
  useGetProjectsQuery,
  useGetProjectByIdQuery,
  useAddProjectMutation,
  useDeleteProjectMutation,
  useAddElementsToProjectMutation,
  useDeleteElementsFromProjectMutation,
} = projectsApi