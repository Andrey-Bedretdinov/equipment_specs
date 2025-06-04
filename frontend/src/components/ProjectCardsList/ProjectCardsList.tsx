import { useGetProjectsQuery } from "../../redux/services/projectsApi"
import ProjectCard from "../ProjectCard/ProjectCard";

const ProjectCardsList: React.FC = () => {

    const { data } = useGetProjectsQuery();

    return (
        <>
            {data?.map((project) => 
                <ProjectCard key={project.id} project={project}/>
            )}
        </>
    )
}

export default ProjectCardsList;