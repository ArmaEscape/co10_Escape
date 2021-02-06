params["_center","_rotation",["_templateType","Undefined"]];
//private _templateIndex = A3E_Templates findIf {([_x,"Name",""] call BIS_fnc_getFromPairs) == _templateName};
private _templates = A3E_Templates select {([_x,"Type",""] call BIS_fnc_getFromPairs) == _templateType};


if(count _templates == 0) exitWith {
	diag_log ("Escape Error: Could not find as signgle template of type "+_templateType);
};
private _template = selectRandom _templates;

//Convert center to ASL
//_center = AGLtoASL _center;

private _hasAttribute = {
	params["_atr","_key"];
	private _index = _atr # 0 find toLower(_key);
	private _return = false;
	if(_index>=0) then {
		_return = true;
	};
	_return;
};
private _getAttribute = {
	params["_atr","_key","_default"];
	private _index = (_atr # 0) find toLower(_key);
	private _return = _default;
	if(_index>=0) then {
		_return = _atr # 1 # _index;
	};
	_return;
};
private _clearance =  [_template,"Clearance",[]] call BIS_fnc_getFromPairs;
if(count(_clearance)>0) then {
	private _tobj =  nearestTerrainObjects [_center, [], (_clearance#0) max (_clearance#1), false, true];
	//[a, b, angle, isRectangle, c]
	private _check = [_center,(_clearance#0),(_clearance#1),(_clearance#2)+_rotation,(_clearance#3)];
	{
		if((getpos _x) inArea _check) then {
			[_x, true] remoteExec ["hideObject", 0, true];
		};
	} forEach _tobj;
};



private _templateObjects =  [_template,"Objects",[]] call BIS_fnc_getFromPairs;
if(count(_templateObjects)==0) exitwith {diag_log ("Escape Error: Template "+_templateName+" contains no objects.");};

private _parkedVehicles = [];
private _statics = [];
private _ammoboxes = [];
private _flags = [];
{
	_x params ["_type","_pos","_dir","_atr"];
	private _realPos = [_center,_center vectorAdd _pos,_rotation] call A3E_fnc_rotatePosition;
	
	
	if([_atr,"Spawn",true] call _getAttribute) then {
		private _obj = _type createvehicle _realPos;
		_obj setdir (_dir+_rotation);
		if([_atr,"AbsoluteHeight",false] call _getAttribute) then {
			private _height = ((AGLtoASL _center) #2) + (_realPos # 2);
			_obj setPosASL [_realPos # 0, _realPos # 1,_height];
		} else {
			_obj setPosATL _realPos;
		};
		//A3E_ListOfCreatedObj pushback _obj;
		if([_atr,"Terminal",false] call _getAttribute) then {
			_obj allowdamage false;
			_obj setvariable ["A3E_isTerminal",true,true];
			[_obj,"green","green","green"] call BIS_fnc_DataTerminalColor;
		};
		if([_atr,"Indestructable",false] call _getAttribute) then {
			_obj allowdamage false;
		};
		if([_atr,"Yeet"] call _hasAttribute) then {
			_obj spawn {
				sleep 2;
				_this setvelocity [0,0,100];
			};
		};
		if([_atr,"Inflame",false] call _getAttribute) then {
			_obj inflame true;
		};
		if([_atr,"Flag",false] call _getAttribute) then {
			_flags pushBack _obj;
		};
		private _init = [_atr,"Init",""] call _getAttribute;
		_obj call compile _init;
	} else {
		if([_atr,"ParkedVehicle",false] call _getAttribute) then {
			private _type = [_atr,"ParkedVehicleType","Unknown"] call _getAttribute;
			private _init = [_atr,"Init",""] call _getAttribute;
			_parkedVehicles pushBack [_type,_realPos,_dir,_init];
		};
		if([_atr,"Static",false] call _getAttribute) then {
			private _type = [_atr,"StaticType","Unknown"] call _getAttribute;
			private _init = [_atr,"Init",""] call _getAttribute;
			_statics pushBack [_type,_realPos,_dir,_init];
		};
		if([_atr,"Ammobox",false] call _getAttribute) then {
			private _type = [_atr,"AmmoType","Unknown"] call _getAttribute;
			private _init = [_atr,"Init",""] call _getAttribute;
			_ammoboxes pushBack [_type,_realPos,_dir,_init];
		};
	};
} foreach _templateObjects;

private _return = [["ParkedVehicles",_parkedVehicles],["Statics",_statics],["Ammoboxes",_ammoboxes],["Flags",_flags]];
_return;