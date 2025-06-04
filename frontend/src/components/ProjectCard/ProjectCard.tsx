import React from "react"
import styles from './ProjectCard.module.css'
import { Card, Typography } from "antd"
import type { IProject } from "../../types/types";
import { useNavigate } from "react-router-dom";
import { useGetProjectKtsLinksQuery } from "../../redux/services/ktsApi";

const { Text } = Typography;

interface ProjectCardProps {
    project: IProject;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {

    const navigate = useNavigate();
    const { data } = useGetProjectKtsLinksQuery(project.id);
    if (data) {
        console.log(`data проекта ${project.id}`, data);
    }


    return (
        <Card
            className={styles.card}
            onClick={() => navigate(`/projects/${project.id}`)}
            title={
                <Text strong>{project.name}</Text>
            }
        >
            <Text>{project.description}</Text>
        </Card>
    )
}

export default ProjectCard;