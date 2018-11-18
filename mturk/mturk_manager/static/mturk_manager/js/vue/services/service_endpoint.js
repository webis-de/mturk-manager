import axios from 'axios';

class Service_Endpoint {
	constructor(token) 
	{
		this.is_initialized = false;
		this.axios = undefined;
		this.callback_connection_error = undefined;
	}

	init(token_instance, callback_connection_error)
	{
		if(this.is_initialized == true)
		{
	 		console.error('Service Endpoint is already initialized!');
			return;
		}

		this.is_initialized = true;

		this.axios = axios.create({
            headers: {
                Authorization: `Token ${token_instance}`,
                'Content-Type': 'application/json',
            }
		});

		this.callback_connection_error = callback_connection_error;
	}

	async make_request({url, method, data}) 
	{
        let config = {
            method: method,
            url: url,
            data: JSON.stringify(data),
        };

        const object_response = {
            success: undefined,
            response: undefined,
            exception: undefined,
            data: undefined,
        };

        try {
            object_response.response = await this.axios.request(config);
            object_response.success = true;
            object_response.data = object_response.response.data;
        } catch(exception) {
            object_response.exception = exception;
            object_response.success = false;
        } 

        if(object_response.success == false)
        {
            if(object_response.exception.message == 'Network Error') {
            	this.callback_connection_error();
            }
        }

        console.log('object_response', object_response)

        return object_response;
	}
 }

export default new Service_Endpoint();
