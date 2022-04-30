export interface IPortfolio {
    id: number;
    name: string;
    broker: IBroker
    broker_id: number;
}

export interface IBroker {
    id: number;
    name: string;
}