import { Refine } from "@pankod/refine-core";
import {
    notificationProvider,
    ReadyPage,
    ErrorComponent,
    LoginPage,
} from "@pankod/refine-antd";
import "@/styles/antd.less";
import routerProvider from "@pankod/refine-react-router-v6";
import dataProvider from "@/lib/graphql";
import { GraphQLClient } from "graphql-request";
import { authProvider } from "@/authProvider";
import {
    Title,
    Header,
    Sider,
    Footer,
    Layout,
    OffLayoutArea,
} from "@/components/layout";
import { useTranslation } from "react-i18next";
import { PortfolioList, PortfolioShow, PortfolioEdit, PortfolioCreate } from "@/pages/portfolio";
import { BrokerList, BrokerShow, BrokerCreate, BrokerEdit } from "@/pages/broker";
import config from '@/./config'

const client = new GraphQLClient(config.API_URL);
const gqlDataProvider = dataProvider(client);


function App() {
    const {t, i18n} = useTranslation();

    const i18nProvider = {
        translate: (key: string, params: object) => t(key, params),
        changeLocale: (lang: string) => i18n.changeLanguage(lang),
        getLocale: () => i18n.language,
    };

    return (
        <Refine
            notificationProvider={notificationProvider}
            ReadyPage={ReadyPage}
            catchAll={<ErrorComponent/>}
            routerProvider={routerProvider}
            dataProvider={gqlDataProvider}
            authProvider={authProvider}
            LoginPage={LoginPage}
            Title={Title}
            Header={Header}
            Sider={Sider}
            Footer={Footer}
            Layout={Layout}
            OffLayoutArea={OffLayoutArea}
            i18nProvider={i18nProvider}
            resources={[
                {
                    name: "brokers",
                    list: BrokerList,
                    show: BrokerShow,
                    edit: BrokerEdit,
                    create: BrokerCreate,
                    canDelete: true,
                },
                {
                    name: "portfolios",
                    list: PortfolioList,
                    show: PortfolioShow,
                    edit: PortfolioEdit,
                    create: PortfolioCreate,
                    canDelete: true,
                },
            ]}
        />
    );
}

export default App;
