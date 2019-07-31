
const server = () =>
{	const 	path 	=	require('path');
	const	express	= 	require('express');
	const	mysql	= 	require('mysql');
	
	const	app 	= 	express();
	const 	router 	= 	express.Router();
	
	const	dbc = mysql.createConnection({ host: "localhost", 
			user: "username", password: "password", 
			database: "spinozalibrary" });
	
	app.get('/catalog', (request, response)	=>
	{
		response.sendFile(path.join(__dirname + '/index.html')) 
	});
	
	app.get('/api/books', (request, response)	=>
	{ 	
		let statement = "SELECT * FROM Books"
		dbc.query(statement, (error, results, fields) =>
		{	
			if (error) { console.log(error); dbc.end(); return; }
			else { response.json(results); }
			dbc.end();
		}) 
	})
				
	app.listen('4444', () => 
	{ console.log("Listening at port 4444")}) }

if (require.main === module) { server();}
	
