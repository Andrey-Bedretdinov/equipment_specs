
import type { IKts } from "../../types/types";
import KtsCard from "../KtsCard/KtsCard";

interface KtsCardsListProps {
    kts_list: IKts[];
}
const KtsCardsList: React.FC<KtsCardsListProps> = ({kts_list}) => {

    return (
        <>
            {kts_list.map((kts) => 
                <KtsCard key={kts.id} kts={kts}/>
            )}
        </>
    )

}

export default KtsCardsList;