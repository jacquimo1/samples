<?php 
/* 
 *		todo:
 * 			- tighten up validation
 * 		 	- handle session with secure cookies
 * 			- connect messenger, generate keys
 * 			- fix handler
 * 			- separate code from html
*/ 	


function insert_user($user) {
	require_once('connect.php');
	$connection = connect();
	if (!$connection) {
		return 'Database connection failed.';
	}
	$result =   pg_query_params($connection, 'INSERT INTO users (userid, username, hashedpassword) VALUES ($1, $2, $3)', $user);
	return $result; 
}

function prepare_user_array() {
	$user = array();
	$userid = md5(uniqid($_POST['username'], true));
	$unique_id = check_uniqueness($userid, $column = 'userid');
	while ($unique_id != 'ok') {
		$userid = md5(uniqid($user['username'], true));
		$unique_id = check_uniqueness($userid, $column = 'userid');
	}
	$user['userid'] = $userid;
	$user['username'] = $_POST['username'];
	$user['hashedpassword'] = password_hash($_POST['password1'], PASSWORD_DEFAULT);
	return $user;
}

function check_pw_match($pw1, $pw2) {
	if ($pw1 == $pw2) {
		return true;
	} 
	else {
		return false;
	}
}

function check_pw_length($pw) {
	if ((strlen($pw) > 10) && (strlen($pw) < 128)) {
		return true;
	} 
	else {
		return false;
	}
}
 
function show_password_fields($response) {
	echo $response['content']['password-fields'];
}
 
function set_password_fields(&$response) {
	$response['content']['password-fields'] = '<tr><td><input type="password" name="password1" maxlength="50" placeholder="password"></td>
		<tr><td><input type="password" name="password2" maxlength="128" placeholder="confirm password"></td>';
}

function show_form_value($response) {
	echo $response['content']['form-value']; 
}

function set_form_value(&$response, $val) {
	$response['content']['form-value'] = $val;
}

function show_placeholder($response) {
	echo $response['content']['username-placeholder']; 
}

function set_placeholder(&$response, $un) {
	$response['content']['username-placeholder'] = $un;
} 
 
function check_uniqueness($value, $column = 'username') {
	require_once('connect.php');
	if (($column) && ($column == 'userid')) {
		$statement = "SELECT * FROM users WHERE userid=$1;";
	}
	else {
		$statement = "SELECT * FROM users WHERE username=$1;";
	}
	
	$connection = connect();
	if (!$connection) {
		return 'Database connection failed.';
	}
	$result = pg_query_params($connection, $statement, array($value));
	$row = pg_fetch_array($result);
	if ($row) {
		return $column . ' is already taken.';
	}
	else {
		return 'ok';
	}
}			
 
function check_un_length($un) {
	if ((strlen($un) > 2) && (strlen($un) < 50))  {
		return true;
	} 
	else {
		return false;
	}
}
 
function show_messages($response) {
	echo '<table>';
	foreach ($response['messages'] as $number) {
		foreach ($number as $message) {
			echo '<tr><td>' . $message . '</td></tr></table>';
		}
	}
}
 
function process_username(&$response) {
	$response['messages'] = array();
	$count = 0;
	foreach ($_POST as $k => $v) {
		if (!$v) {
			$count++;
			$response['messages'][$count] = array($k => 'username is required <br>');
			return false;
		}
		if ($k == 'username') {
			$un_length = check_un_length($v);
			if  (!$un_length) {
				$count++;
				$response['messages'][$count] = array($k => 'username must be three to fifty characters <br>');
				return false;
			}
			else {
				$un_query = check_uniqueness($v);
				if ($un_query != 'ok') {
					$count++;
					$response['messages'][$count] = array($k => $un_query);
					return false;
				}
				else {
					set_form_value($response, $v);
					return true;
				}
			}
		}
	}
}
function process_password(&$response) {
	foreach ($_POST as $k => $v) {
		$count = 0;
		if (!$v) {
			$count++;
			$response['messages'][$count] = array($k => 'password is required <br>');
			return false;
		}
		if ($k == 'password1') {
			$pw_length = check_pw_length($v);
			if (!$pw_length) {
				$count++;
				$response['messages'][$count] = array($k => 'password must be between ten and fifty characters <br>');
				return false;
			}
		}
		if ($k == 'password2') {
			$pw_match = check_pw_match($_POST['password1'], $_POST['password2']);
			if (!$pw_match) {
				$response['messages'][$count] = array($k => 'passwords must match<br>');
				return false;
			}
			else {
				//set_form_value($response, $response['content']['username-placeholder']);
				return true;
			}	
		}
	} 
 }
 
function sign_up(&$response) {
	$username = process_username($response);
	if ($username) {
		set_password_fields($response);
		$password = process_password($response);
		if ($password) {
			$user = prepare_user_array();
			$inserted = insert_user($user);
			if ($inserted) {
				
			}
		}
	}	
}
 
function handler(&$response) {	
	switch($_SERVER["REQUEST_METHOD"]) {
	case 'POST': 
		sign_up($response);
		break;
	case 'GET': 
		break;
	default:
		echo "Neither POST nor GET received."; 
		break;
	}
}

$response = array('messages' => array(), 'content' => array('password-fields' => '',  'form-value' => ''));
handler($response);
?>

<!DOCTYPE HTML>
<html>
  <head>
	<link rel="stylesheet" href="style.css">
  </head>
  <body>
  <div id="sign_up">
	<form method='post' action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']);?>">
	  <table>
			<h2>sign up</h2>
			<tr>
				<td><input type="text" name="username" maxlength="50" value = "<?php show_form_value($response);?>" placeholder="username"></td>
			</tr>
		<?php show_password_fields($response);?>
	  </table>
	  <input type="submit" value="check">
	</form>
	<br><br>
	<?php show_messages($response)?>
</div>
</body>
</html>
