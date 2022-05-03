import {
    Create,
    Form,
    Input,
    useForm,
} from "@pankod/refine-antd";

import { IBroker } from "interfaces";

export const BrokerCreate = () => {
    const { formProps, saveButtonProps } = useForm<IBroker>({
    });

    return (
        <Create saveButtonProps={saveButtonProps}>
            <Form {...formProps} layout="vertical">
                <Form.Item label="Name" name="name"
                           rules={[
                               {
                                   required: true,
                               },
                           ]}>
                    <Input />
                </Form.Item>
            </Form>
        </Create>
    );
};
